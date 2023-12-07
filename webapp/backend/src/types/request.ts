import { Request } from 'express';

export type RequestWithUser = {
  user: {
    id: string,
    email: string
  }
}
