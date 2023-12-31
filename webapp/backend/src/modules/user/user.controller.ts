import {
  Body,
  Controller,
  HttpException,
  HttpStatus,
  Post,
} from '@nestjs/common';
import { UserService } from './user.service';
import { SignUpBody, ConfirmSignUpBody, SignInBody } from './types/requestBody';
import { Response } from '../../types/response';
import {
  AuthenticationResultType,
  InitiateAuthCommandOutput,
} from '@aws-sdk/client-cognito-identity-provider';
import { verifyIdToken } from '../../auth/verifier';
import { User } from '../../types/request';

@Controller('user')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('sign-in')
  async signIn(
    @Body() body: SignInBody,
  ): Promise<Response<AuthenticationResultType & { user: User }>> {
    let data: InitiateAuthCommandOutput;
    try {
      data = await this.userService.signIn(body.username, body.password);
    } catch (e) {
      throw new HttpException(e.message, HttpStatus.BAD_REQUEST);
    }

    if (!data.AuthenticationResult || !data.AuthenticationResult.IdToken) {
      throw new HttpException(
        'Error occurred while processing request.',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }

    const userData = await verifyIdToken(data.AuthenticationResult.IdToken);

    return {
      status: true,
      data: {
        ...data.AuthenticationResult,
        user: {
          id: userData.sub,
          email: userData.email as string,
        },
      },
    };
  }

  @Post('sign-up')
  async signUp(@Body() body: SignUpBody) {
    try {
      await this.userService.signUp(body.username, body.password);
    } catch (e) {
      throw new HttpException(e.message, HttpStatus.BAD_REQUEST);
    }

    return {
      status: true,
      data: 'Account created',
    };
  }

  @Post('confirm-sign-up')
  async confirmSignUp(
    @Body() body: ConfirmSignUpBody,
  ): Promise<Response<string>> {
    try {
      await this.userService.confirmSignUp(
        body.username,
        body.confirmationCode,
      );
    } catch (e) {
      throw new HttpException(e.message, HttpStatus.BAD_REQUEST);
    }

    return {
      status: true,
      data: 'Account confirmed',
    };
  }
}
