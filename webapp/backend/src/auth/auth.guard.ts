import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';
import { Request } from 'express';
import { CognitoJwtVerifier } from 'aws-jwt-verify';
import { env } from 'process';

@Injectable()
export class AuthGuard implements CanActivate {
  private verifier;

  constructor() {
    this.verifier = CognitoJwtVerifier.create({
      userPoolId: env.AWS_COGNITO_USER_POOL_ID as string,
      tokenUse: 'id',
      clientId: env.AWS_COGNITO_CLIENT_ID,
    });
  }

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractTokenFromHeader(request);
    if (!token) {
      throw new UnauthorizedException();
    }
    try {
      // @ts-expect-error verify method expect 2 argument which is error in typings
      const payload = await this.verifier.verify(token);

      request['user'] = {
        id: payload.sub,
        email: payload.email,
      };
    } catch (e) {
      throw new UnauthorizedException();
    }

    return true;
  }

  private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
  }
}
