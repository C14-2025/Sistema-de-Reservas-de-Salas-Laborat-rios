import type { ILab } from "../interfaces/lab";
import { BaseRepository } from "./base";

export class LabRepository extends BaseRepository {
  constructor() {
    super("labs");
  }

  async GetAll(): Promise<ILab[] | null> {
    const response = await fetch(`${this.baseUrl}/${this.path}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) return null;

    const payload: ILab[] = await response.json();
    return payload;
  }
}
