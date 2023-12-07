export type SignInBody = {
  username: string,
  password: string
}

export type SignUpBody = {
  username: string,
  password: string
}

export type ConfirmSignUpBody = {
  username: string,
  confirmationCode: string
}
