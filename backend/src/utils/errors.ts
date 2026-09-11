export class AppError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code = 'APPLICATION_ERROR',
  ) {
    super(message);
  }
}
