import {
  Controller,
  FileTypeValidator,
  HttpException,
  HttpStatus,
  ParseFilePipe,
  Post,
  UploadedFile,
  UseGuards,
  UseInterceptors,
  Req,
} from '@nestjs/common';
import { ProcessService } from './process.service';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import e from 'express';
import { unlinkSync } from 'fs';
import { FILE_UPLOAD_DIR } from '../../constants/file';
import { getUploadFilePath } from '../../utils/file';
import { Response } from '../../types/response';
import { v4 } from 'uuid';
import { AuthGuard } from '../../auth/auth.guard';
import { RequestWithUser } from '../../types/request';

@Controller('process')
@UseGuards(AuthGuard)
export class ProcessController {
  constructor(private readonly fileService: ProcessService) {}

  @Post('create')
  @UseInterceptors(
    FileInterceptor('file', {
      storage: diskStorage({
        destination: FILE_UPLOAD_DIR,
        filename(
          req: e.Request,
          file: Express.Multer.File,
          callback: (error: Error | null, filename: string) => void,
        ) {
          callback(null, file.originalname);
        },
      }),
    }),
  )
  async createProcessRequest(
    @Req() request: RequestWithUser,
    @UploadedFile(
      new ParseFilePipe({
        validators: [new FileTypeValidator({ fileType: 'text/csv' })],
      }),
    )
    file: Express.Multer.File,
  ): Promise<Response<string>> {
    const user = request.user;
    const requestUuid = v4();

    try {
      await this.fileService.validateCSVFile(file);
    } catch (e) {
      throw new HttpException(e.message, HttpStatus.BAD_REQUEST);
    }

    // Upload file to S3
    const objectUrl = await this.fileService.uploadFile(file, requestUuid);

    // Add row to DynamoDB
    await this.fileService.addProcessRequestRow(
      requestUuid,
      user.id,
      objectUrl,
    );

    // Add message to SQS
    await this.fileService.sendProcessRequestMessage(
      requestUuid,
      user.id,
      objectUrl,
    );

    // Remove local file
    unlinkSync(getUploadFilePath(file.path));

    return {
      status: true,
      data: requestUuid,
    };
  }
}
