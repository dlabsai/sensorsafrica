import { redirect } from "react-router-dom";
import { getCurrentUser } from "./user";

export const protectedLoader = () => {
  const user = getCurrentUser();
  if (!user) {
    return redirect("/");
  }

  return null;
};
