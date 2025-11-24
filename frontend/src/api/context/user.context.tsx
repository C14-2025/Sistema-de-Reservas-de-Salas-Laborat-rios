import { createContext, useState, type Dispatch, type ReactNode, type SetStateAction, useEffect } from "react";
import type { IUser } from "../interfaces/user";

interface UserProps {
  user: IUser | null;
  isAuth: boolean;
}

interface UserActionProps {
  setUser: Dispatch<SetStateAction<IUser | null>>;
  logout: () => void;
}

type UserContextInterface = UserProps & UserActionProps;

const initialUserState: UserContextInterface = {
  user: null,
  isAuth: false,
  setUser: () => {},
  logout: () => {},
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

  function logout() {
    setUser(null);
    localStorage.removeItem("user"); 
    localStorage.removeItem("token");
  }

  
  useEffect(() => {
    const saved = localStorage.getItem("user");
    if (saved) {
      setUser(JSON.parse(saved));
    }
  }, []);

  return (
    <UserContext.Provider value={{ user, setUser, isAuth, logout }}>
      {children}
    </UserContext.Provider>
  );
}

