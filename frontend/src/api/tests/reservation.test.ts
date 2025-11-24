import { describe, it, expect, beforeEach, vi } from "vitest";
import type { Mock } from "vitest";
import { ReservationRepository } from "../repository/reservation";
import type { IReservation } from "../interfaces/reservation";
import type { ReservationType } from "@/types/reservationType";

describe("ReservationRepository", () => {
  const repo = new ReservationRepository();
  const baseUrl = "http://127.0.0.1:8000/reservations";

  beforeEach(() => {
    global.fetch = vi.fn();
  });

  it("creates a reservation and returns a message", async () => {
    const fakeReservation: IReservation = {
      id: "1",
      user_email: "test@example.com",
      lab_id: "2",
      lab_name: "test",
      date: "2025-01-01",
      start_time: "10:00",
      end_time: "12:00",
      status: "pending",
      message: "reservation created",
    };

    const data: Partial<ReservationType> = {
      id: "1",
      user_email: "test@example.com",
      lab_id: "2",
      date: "2025-01-01",
      start_time: "10:00",
      end_time: "12:00",
      status: "pending",
    };

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeReservation),
    });

    const result = await repo.Create(data);

    expect(fetch).toHaveBeenCalledWith(baseUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    expect(result).toEqual(fakeReservation);
  });

  it("returns null when reservation creation fails", async () => {
    const data: Partial<ReservationType> = {
      id: "1",
      user_email: "test@example.com",
      lab_id: "2",
      date: "2025-01-01",
      start_time: "10:00",
      end_time: "12:00",
      status: "pending",
    };

    (fetch as unknown as Mock).mockResolvedValueOnce({ ok: false });

    const result = await repo.Create(data);

    expect(result).toBeNull();
  });

  it("returns all reservations", async () => {
    const fakeReservations: IReservation[] = [
      {
        id: "1",
        user_email: "test@example.com",
        lab_id: "2",
        lab_name: "test",
        date: "2025-01-01",
        start_time: "10:00",
        end_time: "12:00",
        status: "pending",
        message: "reservation created",
      },
      {
        id: "2",
        user_email: "test@example.com",
        lab_id: "3",
        lab_name: "test3",
        date: "2025-01-01",
        start_time: "10:00",
        end_time: "12:00",
        status: "pending",
        message: "reservation created",
      },
    ];

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeReservations),
    });

    const result = await repo.GetAll();

    expect(fetch).toHaveBeenCalledWith(baseUrl, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    expect(result).toEqual(fakeReservations);
  });

  it("returns null when GetAll fails", async () => {
    (fetch as unknown as Mock).mockResolvedValueOnce({ ok: false });

    const result = await repo.GetAll();

    expect(result).toBeNull();
  });

  it("gets reservations by user", async () => {
    const fakeReservations: IReservation[] = [
      {
        id: "1",
        user_email: "test@example.com",
        lab_id: "3",
        lab_name: "Chem Lab",
        date: "2025-02-01",
        start_time: "10:00",
        end_time: "12:00",
        status: "pending",
        message: "ok",
      },
    ];

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeReservations),
    });

    const result = await repo.GetByUser("test@example.com");

    expect(fetch).toHaveBeenCalledWith(`${baseUrl}/user/test@example.com`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    expect(result).toEqual(fakeReservations);
  });

  it("returns null when GetByUser fails", async () => {
    (fetch as unknown as Mock).mockResolvedValueOnce({ ok: false });

    const result = await repo.GetByUser("test@example.com");

    expect(result).toBeNull();
  });

  it("gets a reservation by ID", async () => {
    const fakeReservation: IReservation = {
      id: "123",
      user_email: "test@example.com",
      lab_id: "9",
      lab_name: "Lab 9",
      date: "2025-03-01",
      start_time: "14:00",
      end_time: "16:00",
      status: "approved",
      message: "ok",
    };

    (fetch as unknown as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve(fakeReservation),
    });

    const result = await repo.Get("123");

    expect(fetch).toHaveBeenCalledWith(`${baseUrl}/123`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    expect(result).toEqual(fakeReservation);
  });

  it("returns null when Get fails", async () => {
    (fetch as unknown as Mock).mockResolvedValueOnce({ ok: false });

    const result = await repo.Get("123");

    expect(result).toBeNull();
  });
});
