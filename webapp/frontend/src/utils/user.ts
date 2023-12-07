import { User } from "../types/user";

const LOCAL_STORAGE_KEY = "currentUser";
let user: User | undefined;

export const getCurrentUser = () => {
  if (!user) {
    user = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)!);
  }

  return user;
};

export const setUser = (newUser: User) => {
  user = newUser;
  localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(newUser));
};

export const clearUser = () => {
  user = undefined;
  localStorage.removeItem(LOCAL_STORAGE_KEY);
};
