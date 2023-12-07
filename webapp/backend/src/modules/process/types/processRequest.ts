export type ProcessRequest = {
  RequestID: string;
  UserID: string;
  S3location: string;
  InferenceS3location?: string;
  Status: 'Processing' | 'Finished' | 'Failed';
  ErrorMsg?: string;
};
