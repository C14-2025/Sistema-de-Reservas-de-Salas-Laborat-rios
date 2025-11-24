import type { ReservationType } from "@/types/reservationType";
import type { IReservation } from "../interfaces/reservation";
import { BaseRepository } from "./base";

export class ReservationRepository extends BaseRepository {
  constructor() {
    super("reservations");
  }

  async Create(
    data: Partial<ReservationType>
  ): Promise<{ message: string } | null> {
    const response = await fetch(`${this.baseUrl}/${this.path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      return null;
    }

    const payload: IReservation = await response.json();
    return payload;
  }

  async GetAll(): Promise<IReservation[] | null> {
    const response = await fetch(`${this.baseUrl}/${this.path}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) return null;

    const payload: IReservation[] = await response.json();
    return payload;
  }

  async GetByUser(email: string): Promise<IReservation[] | null> {
    const response = await fetch(`${this.baseUrl}/${this.path}/user/${email}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) return null;

    const payload: IReservation[] = await response.json();
    return payload;
  }

  async Get(reservationId: string): Promise<IReservation | null> {
    const response = await fetch(
      `${this.baseUrl}/${this.path}/${reservationId}`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );
    if (!response.ok) return null;

    const payload: IReservation = await response.json();
    return payload;
  }
}
