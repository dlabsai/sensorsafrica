import { useEffect } from "react";
import { clearUser } from "../../utils/user";
import { useNavigate } from "react-router-dom";

function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    clearUser();
    navigate("/");
  }, []);

  return null;
}

export default Logout;
