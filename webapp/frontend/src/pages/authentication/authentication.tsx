import React, { useEffect, useState } from "react";
import "./Authentication.css";
import { getCurrentUser, setUser } from "../../utils/user";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import {
  Layout,
  Image,
  Input,
  Form,
  Button,
  Typography,
  Space,
  message as Toast,
} from "antd";
import { useNavigate } from "react-router-dom";
import { confirmSignUp, signIn, signUp } from "../../services/authentication";
import DLabsFooter from "../../Components/footer";

type FieldType = {
  email?: string;
  password?: string;
  confirmationCode?: string;
};

function Authentication() {
  const navigate = useNavigate();
  const [isLoginForm, setIsLoginForm] = useState(true);
  const [isRegisterConfirmForm, setIsRegisterConfirmForm] = useState(false);
  const [formErrors, setFormErrors] = useState<string[]>([]);

  useEffect(() => {
    const user = getCurrentUser();

    if (user) {
      navigate("/dashboard");
    }
  }, []);

  const signInUser = async (email: string, password: string) => {
    setFormErrors([]);

    try {
      const user = await signIn(email, password);
      setUser(user);
      navigate("/dashboard");
    } catch (e) {
      if ("message" in (e as { message: string })) {
        setFormErrors([(e as { message: string }).message]);
      }

      if ((e as { message: string }).message === "User is not confirmed.") {
        setIsLoginForm(false);
        setIsRegisterConfirmForm(true);
      }
    }
  };

  const signUpUser = async (email: string, password: string) => {
    setFormErrors([]);

    try {
      await signUp(email, password);
      setIsRegisterConfirmForm(true);
    } catch (e) {
      if ("message" in (e as { message: string })) {
        setFormErrors([(e as { message: string }).message]);
      }
    }
  };

  const confirmSignUpUser = async (email: string, confirmationCode: string) => {
    setFormErrors([]);

    try {
      await confirmSignUp(email, confirmationCode);

      Toast.success("Account activated, you can log in now.");
      onLoginButtonClick();
    } catch (e) {
      if ("message" in (e as { message: string })) {
        setFormErrors([(e as { message: string }).message]);
      }
    }
  };

  const onRegisterButtonClick = () => {
    setIsLoginForm(false);
    setFormErrors([]);
  };

  const onLoginButtonClick = () => {
    setIsLoginForm(true);
    setIsRegisterConfirmForm(false);
    setFormErrors([]);
  };

  const getForm = (isLogin: boolean) => {
    return (
      <div key={isLogin ? "login" : "register"}>
        <Form
          name="login"
          className="login-form"
          onFinish={(a) => {
            if (isLogin) {
              signInUser(a.email, a.password);
            } else {
              if (!isRegisterConfirmForm) {
                signUpUser(a.email, a.password);
              } else {
                confirmSignUpUser(a.email, a.confirmationCode);
              }
            }
          }}
          autoComplete="off"
        >
          <h3>{isLogin ? "Login" : "Register"}</h3>
          <Form.Item<FieldType>
            name="email"
            rules={[{ required: true, message: "Please input your Email!" }]}
          >
            <Input
              prefix={<UserOutlined className="site-form-item-icon" />}
              type="email"
              placeholder="Email"
            />
          </Form.Item>

          <Form.Item<FieldType>
            name="password"
            rules={[{ required: true, message: "Please input your Password!" }]}
          >
            <Input
              prefix={<LockOutlined className="site-form-item-icon" />}
              type="password"
              placeholder="Password"
            />
          </Form.Item>

          {!isLogin && isRegisterConfirmForm && (
            <>
              <Typography.Text type="success">
                Enter confirmation code from email
              </Typography.Text>
              <Form.Item<FieldType>
                name="confirmationCode"
                rules={[
                  {
                    required: true,
                    message: "Please input Confirmation Code from email!",
                  },
                ]}
              >
                <Input
                  prefix={<LockOutlined className="site-form-item-icon" />}
                  placeholder="Confirmation code"
                />
              </Form.Item>
            </>
          )}

          {formErrors.length > 0 && (
            <Space direction="vertical">
              {formErrors.map((e) => (
                <Typography.Text type="danger">{e}</Typography.Text>
              ))}
            </Space>
          )}

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="login-form-button"
            >
              {isLogin ? "Log in" : "Register"}
            </Button>
            <div className="login-form-register">
              {isLogin ? (
                <>
                  Or{" "}
                  <a href="#" onClick={onRegisterButtonClick}>
                    register now!
                  </a>
                </>
              ) : (
                <>
                  Or{" "}
                  <a href="#" onClick={onLoginButtonClick}>
                    login now!
                  </a>
                </>
              )}
            </div>
          </Form.Item>
        </Form>
      </div>
    );
  };

  return (
    <>
      <Layout className="layout">
        <div>
          <Image
            src="../../assets/shape.svg"
            alt="shape"
            preview={false}
            className="bottom-shape"
          />
        </div>
        <div>
          <Image
            src="../../assets/top-shape.svg"
            alt="shape"
            preview={false}
            className="top-shape"
          />
        </div>
        <h1 className="title">Sensors Africa</h1>
        <h4 className="subtitle">HACK TO THE RESCUE</h4>
        <div className="form-container">
          {isLoginForm && getForm(true)}
          {!isLoginForm && getForm(false)}
        </div>
      </Layout>
      <DLabsFooter />
    </>
  );
}

export default Authentication;
