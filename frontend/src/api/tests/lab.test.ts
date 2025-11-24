import { describe, it, expect, beforeEach, vi } from "vitest";
import type { Mock } from "vitest";
import { LabRepository } from "../repository/lab";
import type { ILab } from "../interfaces/lab";

describe("LabRepository", () => {
  const repo = new LabRepository();
  const baseUrl = "http://127.0.0.1:8000/labs";

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("returns all labs when request is successful", async () => {
    const fakeLabs: ILab[] = [
      {
        id: "1",
        name: "Lab 1",
        description: "Physics lab",
        message: "ok",
      },
      {
        id: "2",
        name: "Lab 2",
        description: "Chemistry lab",
        message: "ok",
      },
    ];

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeLabs),
    });

    const result = await repo.GetAll();

    expect(fetch).toHaveBeenCalledWith(baseUrl, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    expect(result).toEqual(fakeLabs);
  });

  it("returns null when request fails", async () => {
    (fetch as unknown as Mock).mockResolvedValueOnce({ ok: false });

    const result = await repo.GetAll();

    expect(result).toBeNull();
  });
});
