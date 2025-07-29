import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Stack
} from '@mui/material';

function App() {
  const [file, setFile] = useState(null);
  const [patientId, setPatientId] = useState('demo123');
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const res = await axios.get('http://localhost:5000/documents', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setDocuments(res.data);
    } catch (err) {
      alert('Session expired. Please refresh.');
      console.error(err);
    }
  };

  useEffect(() => {
    const login = async () => {
      try {
        const res = await axios.post('http://localhost:5000/login', {
          user: 'demo',
        });
        localStorage.setItem('token', res.data.token);
        fetchDocuments();
      } catch (err) {
        alert('Login failed');
        console.error(err);
      }
    };

    login();
  }, []);

  const handleUpload = async () => {
    if (!file) return alert('Please select a file');
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('patient_id', patientId);
    try {
      await axios.post('http://localhost:5000/documents/upload', formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      alert('Upload successful');
      setFile(null);
      fetchDocuments();
    } catch (err) {
      alert('Upload failed');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (id) => {
    const token = localStorage.getItem('token');
    window.open(`http://localhost:5000/documents/${id}/download?token=${token}`, '_blank');
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/documents/${id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      fetchDocuments();
    } catch (err) {
      alert('Delete failed');
      console.error(err);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        backgroundImage: 'url("/medical-bg.jpg")',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        py: 6,
        px: 2,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <Container maxWidth="md">
        <Paper
          elevation={10}
          sx={{
            p: 4,
            borderRadius: 4,
            background: 'rgba(255,255,255,0.92)',
            boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
            backdropFilter: 'blur(4px)',
          }}
        >
          <Box
            sx={{
              mb: 4,
              py: 2,
              borderRadius: 2,
              background: 'linear-gradient(90deg, #43cea2 0%, #185a9d 100%)',
              color: 'white',
              textAlign: 'center',
              boxShadow: 2,
            }}
          >
            <Typography variant="h3" fontWeight="bold" letterSpacing={2}>
              HealthTech Document Manager
            </Typography>
            <Typography variant="subtitle1" sx={{ mt: 1 }}>
              Securely upload, view, and manage patient PDFs
            </Typography>
          </Box>
          <Box sx={{ mb: 3 }}>
            <Stack direction="row" spacing={2} alignItems="center">
              <Button
                variant="contained"
                color="info"
                component="label"
                sx={{ fontWeight: 'bold', boxShadow: 2 }}
              >
                Select PDF
                <input
                  type="file"
                  accept="application/pdf"
                  hidden
                  onChange={(e) => setFile(e.target.files[0])}
                />
              </Button>
              <TextField
                label="Patient ID"
                value={patientId}
                onChange={(e) => setPatientId(e.target.value)}
                size="small"
                sx={{ background: '#e0f2f1', borderRadius: 1 }}
              />
              <Button
                variant="contained"
                color="success"
                onClick={handleUpload}
                disabled={loading}
                sx={{ fontWeight: 'bold', boxShadow: 2 }}
              >
                {loading ? <CircularProgress size={24} /> : 'Upload PDF'}
              </Button>
              {file && (
                <Typography variant="body2" color="info.main" fontWeight="bold">
                  {file.name}
                </Typography>
              )}
            </Stack>
          </Box>
          <Typography variant="h6" gutterBottom color="primary" fontWeight="bold">
            Uploaded Files
          </Typography>
          <TableContainer component={Paper} sx={{ borderRadius: 2, boxShadow: 1 }}>
            <Table>
              <TableHead>
                <TableRow sx={{ background: '#e0f7fa' }}>
                  <TableCell sx={{ fontWeight: 'bold' }}>Filename</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>Patient ID</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>Upload Date</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>Size (KB)</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 'bold' }}>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {documents.map((doc) => (
                  <TableRow key={doc.id} hover>
                    <TableCell>{doc.filename}</TableCell>
                    <TableCell>{doc.patient_id}</TableCell>
                    <TableCell>{doc.upload_date}</TableCell>
                    <TableCell>{doc.size_kb}</TableCell>
                    <TableCell align="center">
                      <Stack direction="row" spacing={1} justifyContent="center">
                        <Button
                          variant="outlined"
                          color="primary"
                          size="small"
                          onClick={() => handleDownload(doc.id)}
                          sx={{ fontWeight: 'bold' }}
                        >
                          Download
                        </Button>
                        <Button
                          variant="outlined"
                          color="error"
                          size="small"
                          onClick={() => handleDelete(doc.id)}
                          sx={{ fontWeight: 'bold' }}
                        >
                          Delete
                        </Button>
                      </Stack>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Container>
    </Box>
  );
}

export default App;