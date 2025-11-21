import type { AuthType } from "@/types/authType";
import type { IAuth } from "../interfaces/auth";
import { BaseRepository } from "./base";

export class AuthRepository extends BaseRepository {
  constructor() {
    super("auth");
  }

  async Login(data: AuthType): Promise<IAuth | null> {
    const response = await fetch(`${this.baseUrl}/${this.path}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      return null;
    }

    const payload: IAuth = await response.json();
    return payload;
  }
}
