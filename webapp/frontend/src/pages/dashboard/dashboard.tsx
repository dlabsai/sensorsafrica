import React, { useEffect, useMemo, useState } from "react";
import {
  Button,
  Layout,
  Menu,
  message,
  Table,
  Tag,
  Upload,
  UploadProps,
} from "antd";
import { UploadOutlined } from "@ant-design/icons";
import { NavLink } from "react-router-dom";
import { getItems } from "../../services/process";

import "./Dashboard.css";
import { getCurrentUser } from "../../utils/user";
import { User } from "../../types/user";
import DLabsFooter from "../../Components/footer";

const STATUS_COLOR = {
  processing: "blue",
  pending: "lime",
  success: "green",
  failed: "red",
  cancel: "yellow",
};

type TableDataType = {
  S3location: string;
  Status: string;
  InferenceS3location: string;
};

function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    getItems().then((r) => {
      setData(r.data);
    });
  };

  const user = getCurrentUser() as User;

  const props: UploadProps = {
    name: "file",
    accept: "text/csv",
    action: `${process.env.REACT_APP_BACKEND_URL}/process/create`,
    headers: {
      authorization: `Bearer ${user.idToken}`,
    },
    onChange(info) {
      if (info.file.status === "done") {
        loadData();
      } else if (info.file.status === "error") {
        message.error(
          `${info.file.name} file upload failed: ${info.file.response.message}`,
        );
      }
    },
  };

  const columns = useMemo(() => {
    return [
      {
        title: "Request ID",
        dataIndex: "RequestID",
        key: "RequestID",
      },
      {
        title: "Status",
        dataIndex: "Status",
        key: "Status",
        render: (_: any, { Status }: TableDataType) => (
          <Tag
            key={Status}
            color={STATUS_COLOR[Status as keyof typeof STATUS_COLOR]}
          >
            {Status.toUpperCase()}
          </Tag>
        ),
      },
      {
        title: "Original File",
        dataIndex: "S3location",
        key: "S3location",
        render: (_: any, { S3location }: TableDataType) => (
          <a href={S3location} target="_blank" rel="noreferrer">
            Download
          </a>
        ),
      },
      {
        title: "Result File",
        dataIndex: "InferenceS3location",
        key: "InferenceS3location",
        render: (_: any, { InferenceS3location }: TableDataType) =>
          InferenceS3location ? (
            <a href={InferenceS3location} target="_blank" rel="noreferrer">
              Download
            </a>
          ) : (
            <>Not available yet</>
          ),
      },
    ];
  }, []);

  return (
    <>
      <Layout className="dashboard">
        <Menu mode="horizontal">
          <Layout className="header">
            <h2>Sensors Africa</h2>
            <NavLink to={"/logout"}>Logout</NavLink>
          </Layout>
        </Menu>
        <Layout.Content className="content">
          <h2>Add new file to process</h2>
          <Upload {...props}>
            <Button icon={<UploadOutlined />}>Create new Request</Button>
          </Upload>
          <h2>Current requests</h2>
          <Table dataSource={data} columns={columns} />
        </Layout.Content>
      </Layout>
      <DLabsFooter />
    </>
  );
}

export default Dashboard;
