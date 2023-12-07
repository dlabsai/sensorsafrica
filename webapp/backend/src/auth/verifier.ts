import { CognitoJwtVerifier } from 'aws-jwt-verify';
import { env } from 'process';

export const verifyIdToken = (token: string) => {
  const verifier = CognitoJwtVerifier.create({
    userPoolId: env.AWS_COGNITO_USER_POOL_ID as string,
    tokenUse: 'id',
    clientId: env.AWS_COGNITO_CLIENT_ID,
  });

  // @ts-expect-error verify method expect 2 argument which is error in typings
  return verifier.verify(token);
};
