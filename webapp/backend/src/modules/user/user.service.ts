import {Injectable} from "@nestjs/common";
import {
  CognitoIdentityProviderClient,
  ConfirmSignUpCommand,
  InitiateAuthCommand,
  InitiateAuthCommandOutput,
  SignUpCommand,
} from "@aws-sdk/client-cognito-identity-provider";
import { createHmac } from 'crypto';
import {env} from "process";

@Injectable()
export class UserService {
  private cognitoClient: CognitoIdentityProviderClient
  
  constructor() {
    this.cognitoClient = new CognitoIdentityProviderClient({region: env.AWS_S3_REGION})
  }

  async signIn(username: string, password: string): Promise<InitiateAuthCommandOutput> {
    const secretHash = createHmac('sha256', env.AWS_COGNITO_CLIENT_SECRET as string)
      .update(`${username}${env.AWS_COGNITO_CLIENT_ID}`)
      .digest('base64');
    
    try {
      return await this.cognitoClient.send(new InitiateAuthCommand({
        ClientId: env.AWS_COGNITO_CLIENT_ID,
        AuthFlow: 'USER_PASSWORD_AUTH',
        AuthParameters: {
          USERNAME: username,
          PASSWORD: password,
          SECRET_HASH: secretHash,
        }
      }));
    } catch (e) {
      throw Error(e.message);
    }
  }
  
  async signUp(username: string, password: string) {
    const secretHash = createHmac('sha256', env.AWS_COGNITO_CLIENT_SECRET as string)
      .update(`${username}${env.AWS_COGNITO_CLIENT_ID}`)
      .digest('base64');
    
    try {
      await this.cognitoClient.send(new SignUpCommand({
        ClientId: env.AWS_COGNITO_CLIENT_ID,
        Username: username,
        Password: password,
        SecretHash: secretHash
      }));
    } catch (e) {
      throw Error(e.message);
    }
  }
  
  async confirmSignUp(username: string, confirmationCode: string) {
    const secretHash = createHmac('sha256', env.AWS_COGNITO_CLIENT_SECRET as string)
      .update(`${username}${env.AWS_COGNITO_CLIENT_ID}`)
      .digest('base64');
    
    try {
      await this.cognitoClient.send(new ConfirmSignUpCommand({
        ClientId: env.AWS_COGNITO_CLIENT_ID,
        Username: username,
        ConfirmationCode: confirmationCode,
        SecretHash: secretHash
      }));
    } catch (e) {
      throw Error(e.message);
    }
  }
}
