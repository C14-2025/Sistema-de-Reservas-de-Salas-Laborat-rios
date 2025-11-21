import { createContext, useState, type Dispatch, type ReactNode, type SetStateAction } from "react";
import type { IUser } from "../interfaces/user";

interface UserProps {
  user: IUser | null;
  isAuth: boolean;
}

interface UserActionProps {
  setUser: Dispatch<SetStateAction<IUser | null>>;
}

type UserContextInterface = UserProps & UserActionProps;

const initialUserState: UserContextInterface = {
  user: null,
  isAuth: false,
  setUser: () => {},
};

// eslint-disable-next-line react-refresh/only-export-components
export const UserContext =
  createContext<UserContextInterface>(initialUserState);

interface UserProviderProps {
  children: ReactNode;
}

export function UserProvider({ children }: UserProviderProps) {
  const [user, setUser] = useState<IUser | null>(null);
  const isAuth = !!user;

  return (
    <UserContext.Provider value={{ user, setUser, isAuth }}>
      {children}
    </UserContext.Provider>
  );
}

