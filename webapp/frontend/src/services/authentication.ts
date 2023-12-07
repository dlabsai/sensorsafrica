import { User } from "../types/user";
import { request } from "./base";

export const signUp = async (username: string, password: string) => {
  try {
    const result = await request(
      "/user/sign-up",
      "POST",
      JSON.stringify({
        username,
        password,
      }),
    );

    if (!result.status) {
      throw result;
    }

    return result;
  } catch (e) {
    throw e;
  }
};

export const confirmSignUp = async (
  username: string,
  confirmationCode: string,
) => {
  try {
    const result = await request(
      "/user/confirm-sign-up",
      "POST",
      JSON.stringify({
        username,
        confirmationCode,
      }),
    );

    if (!result.status) {
      throw result;
    }

    return result;
  } catch (e) {
    throw e;
  }
};

export const signIn = async (
  username: string,
  password: string,
): Promise<User> => {
  try {
    const result = await request(
      "/user/sign-in",
      "POST",
      JSON.stringify({
        username,
        password,
      }),
    );

    if (!result.status) {
      throw result;
    }

    return {
      id: result.data.user.id,
      email: result.data.user.email,
      idToken: result.data.IdToken,
      refreshToken: result.data.RefreshToken,
    };
  } catch (e) {
    throw e;
  }
};
