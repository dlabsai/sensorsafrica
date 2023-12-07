export class MissingHeadersError extends Error {
  constructor(missingHeaders: string[]) {
    super(`Missing headers: ${missingHeaders.join(', ')}.`);
  }
}
