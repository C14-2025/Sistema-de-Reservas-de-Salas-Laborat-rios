import { describe, it, expect, beforeEach, vi } from "vitest";
import type { Mock } from "vitest";
import { UserRepository } from "../repository/user";
import type { IUser } from "../interfaces/user";
import type { UserType } from "@/types/userType";

describe("UserRepository", () => {
  const repo = new UserRepository();
  const baseUrl = "http://127.0.0.1:8000/user";

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("creates a user and returns IUser", async () => {
    const fakeUser: IUser = {
      name: "John",
      email: "john@example.com",
      message: "ok",
    };

    const data: Partial<UserType> = {
      name: "John",
      email: "john@example.com",
      password: "123456",
    };

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeUser),
    });

    const result = await repo.Create(data);

    expect(fetch).toHaveBeenCalledWith(`${baseUrl}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    expect(result).toEqual(fakeUser);
  });

  it("returns null when user creation fails", async () => {
    const data: Partial<UserType> = {
      name: "John",
      email: "john@example.com",
    };

    (fetch as unknown as Mock).mockResolvedValueOnce({ ok: false });

    const result = await repo.Create(data);

    expect(result).toBeNull();
  });

  it("gets user by ID and returns IUser", async () => {
    const fakeUser: IUser = {
      name: "John",
      email: "john@example.com",
      message: "ok",
    };

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeUser),
    });

    const result = await repo.GetMe("1");

    expect(fetch).toHaveBeenCalledWith(`${baseUrl}/1`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    expect(result).toEqual(fakeUser);
  });

  it("returns null when GetMe fails", async () => {
    (fetch as unknown as Mock).mockResolvedValueOnce({ ok: false });

    const result = await repo.GetMe("1");

    expect(result).toBeNull();
  });
  
});
