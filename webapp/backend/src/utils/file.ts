import * as process from 'process';

export const getUploadFilePath = (filename: string): string => {
  return `${process.cwd()}/${filename}`;
};
