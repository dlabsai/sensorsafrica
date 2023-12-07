export type ProcessRequest = {
  RequestID: string;
  UserID: string;
  S3location: string;
  InferenceS3location?: string;
  Status: 'processing' | 'pending' | 'success' | 'failed' | 'cancel';
  ErrorMsg?: string;
};
