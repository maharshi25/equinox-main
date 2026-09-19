import { getAuthHeaders } from '../utils/authUtils';

// chat api - supports multiple agents
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export type AgentType = 'wellness' | 'productivity' | 'supervisor';

export async function sendChatMessage(
    message: string,
    _port: string = '8000', // kept for backwards compatibility
    agent: AgentType = 'supervisor',
    email?: string | null,
    threadId?: string | null
): Promise<any> {
    // each agent has its own endpoint
    const endpoints: Record<AgentType, string> = {
        wellness: '/api/chat/wellness',
        productivity: '/supervisor',
        supervisor: '/supervisor'
    };

    const endpoint = endpoints[agent] || endpoints.wellness;

    const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ message, email, thread_id: threadId })
    });

    if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
    }

    return res.json();
}

export async function saveThread(
    email: string,
    threadId: string,
    messages: { text: string; sender: string; id: number }[],
    title: string = "New Conversation",
    _port: string = '8000'
): Promise<any> {
    const res = await fetch(`${API_URL}/api/history/${email}/${threadId}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
            messages,
            title
        })
    });

    if (!res.ok) {
        let detail = '';
        try {
            detail = await res.text();
        } catch {
            // ignore body read errors
        }
        const suffix = detail ? `: ${detail}` : '';
        throw new Error(`Failed to save thread (status ${res.status})${suffix}`);
    }
    return res.json();
}

export async function getThread(
    email: string,
    threadId: string,
    _port: string = '8000'
): Promise<any> {
    const res = await fetch(`${API_URL}/api/history/${email}/${threadId}`, {
        headers: getAuthHeaders(),
    });

    if (!res.ok) {
        let detail = '';
        try {
            detail = await res.text();
        } catch {
            // ignore body read errors
        }

        const suffix = detail ? `: ${detail}` : '';

        if (res.status === 401 || res.status === 403) {
            throw new Error(`Unauthorized access to thread (status ${res.status})${suffix}`);
        }

        if (res.status === 404) {
            throw new Error(`Thread not found (status 404)${suffix}`);
        }

        throw new Error(`Failed to fetch thread (status ${res.status})${suffix}`);
    }
    return res.json();
}
