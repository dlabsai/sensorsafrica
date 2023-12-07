import { Request } from 'express';

export type User = {
  id: string;
  email: string;
};

export type RequestWithUser = Request & {
  user: User;
};
