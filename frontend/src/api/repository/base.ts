export class BaseRepository {
  protected path: string;
  protected baseUrl = "http://127.0.0.1:8000";

  constructor(path: string) {
    this.path = path;
  }
}
