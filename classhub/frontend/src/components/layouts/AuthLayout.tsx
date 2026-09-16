import React from 'react';
import { Layout } from 'antd';

const { Content } = Layout;

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <Layout className="min-h-screen bg-gradient-to-br from-primary-500 to-primary-700">
      <Content className="flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">ClassHub</h1>
            <p className="text-primary-100">Class Management System</p>
          </div>
          {children}
        </div>
      </Content>
    </Layout>
  );
};

export default AuthLayout;
