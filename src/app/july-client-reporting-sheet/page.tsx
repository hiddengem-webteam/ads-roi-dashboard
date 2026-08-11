import { Inter } from 'next/font/google';
import JulyClientReportingDashboard from '@/components/JulyClientReportingDashboard';
import '@/components/july/theme.css';

const inter = Inter({ variable: '--font-inter', subsets: ['latin'] });

export default function JulyClientReportingSheetPage() {
  return (
    <div className={`july-theme h-screen ${inter.variable}`}>
      <JulyClientReportingDashboard />
    </div>
  );
}
