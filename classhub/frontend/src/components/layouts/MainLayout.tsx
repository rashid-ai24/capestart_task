import React, { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Avatar, Dropdown, Badge, Space, Typography } from 'antd';
import {
  DashboardOutlined,
  UserOutlined,
  BookOutlined,
  CheckSquareOutlined,
  TrophyOutlined,
  FileTextOutlined,
  DollarOutlined,
  MessageOutlined,
  BarChartOutlined,
  SettingOutlined,
  LogoutOutlined,
  BellOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from '@ant-design/icons';
import { useAppSelector, useAppDispatch } from '../../hooks';
import { logout } from '../../features/auth/authSlice';
import type { MenuProps } from 'antd';

const { Header, Sider, Content } = Layout;
const { Text } = Typography;

const MainLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);

  const menuItems: MenuProps['items'] = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/students',
      icon: <UserOutlined />,
      label: 'Students',
    },
    {
      key: '/courses',
      icon: <BookOutlined />,
      label: 'Courses',
    },
    {
      key: '/attendance',
      icon: <CheckSquareOutlined />,
      label: 'Attendance',
    },
    {
      key: '/grades',
      icon: <TrophyOutlined />,
      label: 'Grades',
    },
    {
      key: '/assignments',
      icon: <FileTextOutlined />,
      label: 'Assignments',
    },
    {
      key: '/fees',
      icon: <DollarOutlined />,
      label: 'Fees',
    },
    {
      key: '/messages',
      icon: <MessageOutlined />,
      label: 'Messages',
    },
    {
      key: '/reports',
      icon: <BarChartOutlined />,
      label: 'Reports',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
  ];

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
      onClick: () => navigate('/profile'),
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
      onClick: () => navigate('/settings'),
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      onClick: () => {
        dispatch(logout());
        navigate('/login');
      },
    },
  ];

  const handleMenuClick = (info: { key: string }) => {
    navigate(info.key);
  };

  return (
    <Layout className="min-h-screen">
      <Sider
        trigger={null}
        collapsible
        collapsed={collapsed}
        width={256}
        collapsedWidth={80}
        className="fixed left-0 top-0 bottom-0 z-10 shadow-md"
      >
        <div className="h-16 flex items-center justify-center border-b border-neutral-200">
          {collapsed ? (
            <div className="text-xl font-bold text-primary-500">CH</div>
          ) : (
            <div className="text-xl font-bold text-primary-500">ClassHub</div>
          )}
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
          className="border-r-0"
        />
      </Sider>
      
      <Layout className={`ml-${collapsed ? '20' : '64'} transition-all duration-300`}>
        <Header className="bg-white shadow-sm px-6 flex items-center justify-between sticky top-0 z-10">
          <div className="flex items-center">
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="text-lg hover:text-primary-500 transition-colors"
            >
              {collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            </button>
          </div>
          
          <div className="flex items-center space-x-4">
            <Badge count={5} size="small">
              <button className="text-lg hover:text-primary-500 transition-colors">
                <BellOutlined />
              </button>
            </Badge>
            
            <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
              <div className="flex items-center space-x-2 cursor-pointer hover:bg-neutral-50 px-3 py-2 rounded-md transition-colors">
                <Avatar size="small" icon={<UserOutlined />} />
                <div className="hidden md:block">
                  <Text className="text-sm font-medium">
                    {user?.first_name} {user?.last_name}
                  </Text>
                  <Text className="text-xs text-neutral-500 block">
                    {user?.role}
                  </Text>
                </div>
              </div>
            </Dropdown>
          </div>
        </Header>
        
        <Content className="p-6">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
