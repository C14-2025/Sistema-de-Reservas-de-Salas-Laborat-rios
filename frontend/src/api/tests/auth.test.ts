import { describe, it, expect, beforeEach, vi } from "vitest";
import type { Mock } from "vitest";
import { AuthRepository } from "../repository/auth";
import type { IAuth } from "../interfaces/auth";
import type { AuthType } from "@/types/authType";

describe("AuthRepository", () => {
  const repo = new AuthRepository();
  const loginUrl = "http://127.0.0.1:8000/auth/login";

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("returns IAuth when login is successful", async () => {
    const fakeAuth: IAuth = {
      id: "123",
      message: "ok"
    };

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeAuth),
    });

    const data: AuthType = { email: "email@email.com", password: "pass" };
    const result = await repo.Login(data);

    expect(fetch).toHaveBeenCalledWith(loginUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    expect(result).toEqual(fakeAuth);
  });

  it("returns null when login fails", async () => {
    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: false,
    });

    const data: AuthType = { email: "email@email.com", password: "wrong" };
    const result = await repo.Login(data);

    expect(result).toBeNull();
  });
});
