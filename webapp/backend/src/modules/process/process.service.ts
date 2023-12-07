import { Injectable } from '@nestjs/common';
import { PutObjectCommand, S3Client } from '@aws-sdk/client-s3';
import {
  DynamoDBClient,
  PutItemCommand,
  ScanCommand,
} from '@aws-sdk/client-dynamodb';
import { SendMessageCommand, SQSClient } from '@aws-sdk/client-sqs';
import { env } from 'process';
import { getUploadFilePath } from '../../utils/file';
import { createReadStream } from 'fs';
import * as mime from 'mime-types';
import { createInterface } from 'readline';
import { REQUIRED_CSV_COLUMNS } from '../../constants/file';
import { MissingHeadersError } from './errors/missingHeadersError';
import { ProcessRequest } from './types/processRequest';
import { marshall, unmarshall } from '@aws-sdk/util-dynamodb';

@Injectable()
export class ProcessService {
  private s3client: S3Client;
  private dynamoDBClient: DynamoDBClient;
  private SQSClient: SQSClient;

  constructor() {
    this.s3client = new S3Client({ region: env.AWS_S3_REGION });
    this.dynamoDBClient = new DynamoDBClient({ region: env.AWS_S3_REGION });
    this.SQSClient = new SQSClient({ region: env.AWS_S3_REGION });
  }

  async uploadFile(
    file: Express.Multer.File,
    requestUuid: string,
  ): Promise<string> {
    const extension = mime.extension(file.mimetype);
    const fileName = `${requestUuid}.${extension}`;

    await this.s3client.send(
      new PutObjectCommand({
        Body: createReadStream(getUploadFilePath(file.path)),
        Bucket: env.AWS_S3_BUCKET,
        Key: fileName,
      }),
    );

    return `https://${env.AWS_S3_BUCKET}.s3.${env.AWS_S3_REGION}.amazonaws.com/${fileName}`;
  }

  async validateCSVFile(file: Express.Multer.File) {
    const stream = createReadStream(getUploadFilePath(file.path));
    const rl = createInterface({
      input: stream,
      crlfDelay: Infinity,
    });

    const firstRow = await new Promise<string>((resolve) => {
      rl.once('line', (line) => {
        resolve(line);

        rl.emit('close');
      });
    });

    const splitCharacter = firstRow.includes(',') ? ',' : ';';
    const headers = firstRow
      .toLowerCase()
      .split(splitCharacter)
      .map((e) => e.replace(/['"]+/g, ''));
    const missingHeaders = REQUIRED_CSV_COLUMNS.filter(
      (e) => !headers.includes(e),
    );

    if (missingHeaders.length > 0) {
      throw new MissingHeadersError(missingHeaders);
    }
  }

  async addProcessRequestRow(
    requestUuid: string,
    userId: string,
    objectUrl: string,
  ) {
    const row: ProcessRequest = {
      RequestID: requestUuid,
      S3location: objectUrl,
      UserID: userId,
      Status: 'Processing',
    };

    await this.dynamoDBClient.send(
      new PutItemCommand({
        TableName: env.AWS_DYNAMODB_TABLE_NAME,
        Item: marshall(row),
      }),
    );
  }

  async sendProcessRequestMessage(
    requestUuid: string,
    userId: string,
    objectUrl: string,
  ) {
    await this.SQSClient.send(
      new SendMessageCommand({
        QueueUrl: env.AWS_SQS_QUEUE_NAME,
        MessageBody: JSON.stringify({
          UserID: userId,
          S3location: objectUrl,
          RequestID: requestUuid,
        }),
      }),
    );
  }

  async getProcessRequestRows(userId: string): Promise<ProcessRequest[]> {
    const result = await this.dynamoDBClient.send(
      new ScanCommand({
        TableName: env.AWS_DYNAMODB_TABLE_NAME,
        ExpressionAttributeValues: {
          ':v1': {
            S: userId,
          },
        },
        FilterExpression: 'UserID = :v1',
      }),
    );

    return (
      result.Items?.map<ProcessRequest>(
        (i) => unmarshall(i) as ProcessRequest,
      ) || []
    );
  }
}
