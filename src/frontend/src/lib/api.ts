const API_URL = "http://10.10.43.61:8000";

export const api = {
    async login(username, password) {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(`${API_URL}/auth/token`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Login failed");
        }

        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        return data;
    },



    async register(userData) {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Registration failed");
        }

        return response.json();
    },

    async analyze(file) {
        const token = localStorage.getItem("token");
        if (!token) {
            throw new Error("Not authenticated");
        }

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${API_URL}/analyze`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Analysis failed");
        }

        return response.json();
    },

    async getHistory() {
        const token = localStorage.getItem("token");
        if (!token) {
            throw new Error("Not authenticated");
        }

        const response = await fetch(`${API_URL}/scans`, {
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error("Failed to fetch history");
        }

        return response.json();
    },

    logout() {
        localStorage.removeItem("token");
    },

    isAuthenticated() {
        return !!localStorage.getItem("token");
    }
};
