import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
const client = new QueryClient();

export default function App() {
  return (
    <QueryClientProvider client={client}>
      <Header />
      <Dashboard />
    </QueryClientProvider>
  );
}
