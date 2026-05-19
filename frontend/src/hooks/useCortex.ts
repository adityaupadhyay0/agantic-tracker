"use client";
import axios from 'axios';
import { useEffect, useState } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function useCortexBCOs() {
    const [bcos, setBcos] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBCOs = async () => {
            try {
                const response = await axios.get(`${API_URL}/bcos/`);
                setBcos(response.data);
            } catch (error) {
                console.error("Error fetching BCOs:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchBCOs();
        const interval = setInterval(fetchBCOs, 10000);
        return () => clearInterval(interval);
    }, []);

    return { bcos, loading };
}
