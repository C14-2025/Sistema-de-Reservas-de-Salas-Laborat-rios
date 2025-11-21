import type { UserType } from "@/types/userType";
import type { IUser } from "../interfaces/user";
import { BaseRepository } from "./base";

export class UserRepository extends BaseRepository {
  constructor() {
    super("user");
  }

  async Create(data: Partial<UserType>): Promise<IUser | null> {
    const response = await fetch(`${this.baseUrl}/${this.path}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      return null;
    }

    const payload: IUser = await response.json();
    return payload;
  }

  async GetMe(userId: string): Promise<IUser | null> {
    const response = await fetch(`${this.baseUrl}/${this.path}/${userId}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!response.ok) {
      return null;
    }

    const payload: IUser = await response.json();
    return payload;
  }
}
