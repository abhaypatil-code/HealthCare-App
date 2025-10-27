// HealthCare App/src/components/admin/ViewPatients.tsx
import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
  CardFooter
} from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuCheckboxItem,
} from '@/components/ui/dropdown-menu';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { MoreHorizontal, FileDown, ListFilter, PlusCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import apiClient from '@/utils/apiClient';
import { PatientUser } from '@/types';
import { Skeleton } from '../ui/skeleton';
import RiskBadge from './RiskBadge'; // We will use this component

type RiskFilter = 'all' | 'diabetes' | 'liver' | 'heart' | 'mental_health';
type RiskLevel = 'all' | 'Low' | 'Medium' | 'High';

const ViewPatients: React.FC = () => {
  const navigate = useNavigate();
  const [patients, setPatients] = useState<PatientUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // State for MVP Filtering
  const [riskFilter, setRiskFilter] = useState<RiskFilter>('all');
  const [riskLevel, setRiskLevel] = useState<RiskLevel>('all');

  const fetchPatients = async () => {
    setLoading(true);
    setError(null);
    try {
      // Build query parameters for filtering
      const params = new URLSearchParams();
      if (riskFilter !== 'all' && riskLevel !== 'all') {
        params.append('risk_filter', riskFilter);
        params.append('risk_level', riskLevel);
      }
      // Default sorting by recency is handled by the backend
      
      const { data } = await apiClient.get('/patients', { params });
      setPatients(data.patients);
    } catch (err) {
      setError('Failed to fetch patients.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch patients when component mounts or filters change
    fetchPatients();
  }, [riskFilter, riskLevel]);
  
  const handleViewDetails = (patientId: number) => {
    navigate(`/admin/patients/${patientId}`);
  };

  const TableSkeleton = () => (
    Array(5).fill(0).map((_, index) => (
      <TableRow key={index}>
        <TableCell><Skeleton className="h-5 w-32" /></TableCell>
        <TableCell><Skeleton className="h-5 w-24" /></TableCell>
        <TableCell><Skeleton className="h-5 w-24" /></TableCell>
        <TableCell><Skeleton className="h-5 w-16" /></TableCell>
        <TableCell><Skeleton className="h-5 w-32" /></TableCell>
        <TableCell><Skeleton className="h-8 w-8" /></TableCell>
      </TableRow>
    ))
  );

  return (
    <Tabs defaultValue="all">
      <div className="flex items-center">
        <TabsList>
          <TabsTrigger value="all">All Patients</TabsTrigger>
          {/* Add more tabs here if needed, e.g., 'High Risk' */}
        </TabsList>
        <div className="ml-auto flex items-center gap-2">
          {/* Risk Filter Dropdowns - Fulfills MVP Requirement */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="sm" className="h-8 gap-1">
                <ListFilter className="h-3.5 w-3.5" />
                <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
                  Filter by Risk
                </span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Filter by Disease</DropdownMenuLabel>
              <DropdownMenuCheckboxItem
                checked={riskFilter === 'all'}
                onCheckedChange={() => setRiskFilter('all')}
              >
                All
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={riskFilter === 'diabetes'}
                onCheckedChange={() => setRiskFilter('diabetes')}
              >
                Diabetes
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={riskFilter === 'liver'}
                onCheckedChange={() => setRiskFilter('liver')}
              >
                Liver
              </DropdownMenuCheckboxItem>
               <DropdownMenuCheckboxItem
                checked={riskFilter === 'heart'}
                onCheckedChange={() => setRiskFilter('heart')}
              >
                Heart
              </DropdownMenuCheckboxItem>
               <DropdownMenuCheckboxItem
                checked={riskFilter === 'mental_health'}
                onCheckedChange={() => setRiskFilter('mental_health')}
              >
                Mental Health
              </DropdownMenuCheckboxItem>
              <DropdownMenuSeparator />
              <DropdownMenuLabel>Filter by Level</DropdownMenuLabel>
              <DropdownMenuCheckboxItem
                checked={riskLevel === 'all'}
                onCheckedChange={() => setRiskLevel('all')}
              >
                All Levels
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={riskLevel === 'Low'}
                onCheckedChange={() => setRiskLevel('Low')}
              >
                Low
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={riskLevel === 'Medium'}
                onCheckedChange={() => setRiskLevel('Medium')}
              >
                Medium
              </DropdownMenuCheckboxItem>
              <DropdownMenuCheckboxItem
                checked={riskLevel === 'High'}
                onCheckedChange={() => setRiskLevel('High')}
              >
                High
              </DropdownMenuCheckboxItem>
            </DropdownMenuContent>
          </DropdownMenu>
          
          <Button size="sm" variant="outline" className="h-8 gap-1">
            <FileDown className="h-3.5 w-3.5" />
            <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
              Export
            </span>
          </Button>
          <Button size="sm" className="h-8 gap-1" onClick={() => navigate('/admin/add-patient')}>
            <PlusCircle className="h-3.5 w-3.5" />
            <span className="sr-only sm:not-sr-only sm:whitespace-nowrap">
              Add Patient
            </span>
          </Button>
        </div>
      </div>
      <TabsContent value="all">
        <Card>
          <CardHeader>
            <CardTitle>Registered Patients</CardTitle>
            <CardDescription>
              A list of all registered patients in the system.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {error && (
              <div className="text-red-500 text-center">{error}</div>
            )}
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Patient Name</TableHead>
                  <TableHead>ABHA ID</TableHead>
                  <TableHead>Overall Risk</TableHead>
                  <TableHead>Age</TableHead>
                  <TableHead>Registered On</TableHead>
                  <TableHead>
                    <span className="sr-only">Actions</span>
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableSkeleton />
                ) : patients.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center">
                      No patients found.
                    </TableCell>
                  </TableRow>
                ) : (
                  patients.map((patient) => (
                    <TableRow key={patient.id}>
                      <TableCell className="font-medium">{patient.full_name}</TableCell>
                      <TableCell>...{patient.abha_id.slice(-4)}</TableCell>
                      <TableCell>
                        <RiskBadge 
                          prediction={patient.risk_prediction} 
                          condensed={true} 
                        />
                      </TableCell>
                      <TableCell>{patient.age}</TableCell>
                      <TableCell>
                        {new Date(patient.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button
                              aria-haspopup="true"
                              size="icon"
                              variant="ghost"
                            >
                              <MoreHorizontal className="h-4 w-4" />
                              <span className="sr-only">Toggle menu</span>
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>Actions</DropdownMenuLabel>
                            <DropdownMenuItem onClick={() => handleViewDetails(patient.id)}>
                              View Details
                            </DropdownMenuItem>
                            <DropdownMenuItem>Edit</DropdownMenuItem>
                            <DropdownMenuItem className="text-destructive">
                              Delete
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
          <CardFooter>
            <div className="text-xs text-muted-foreground">
              Showing <strong>{patients.length}</strong> {patients.length === 1 ? 'patient' : 'patients'}
            </div>
          </CardFooter>
        </Card>
      </TabsContent>
    </Tabs>
  );
};

export default ViewPatients;