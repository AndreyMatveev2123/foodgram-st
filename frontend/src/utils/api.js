const BASE_URL = 'http://localhost:8000/api';

const handleResponse = (res) => {
    if (res.ok) {
        return res.json();
    }
    return Promise.reject(`Ошибка: ${res.status}`);
};

export const register = (email, username, password, first_name, last_name) => {
    return fetch(`${BASE_URL}/users/`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, username, password, first_name, last_name })
    })
    .then(handleResponse);
};

export const login = (email, password) => {
    return fetch(`${BASE_URL}/auth/token/login/`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(handleResponse);
};

export const logout = (token) => {
    return fetch(`${BASE_URL}/auth/token/logout/`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
    .then(handleResponse);
};

export const getRecipes = (token) => {
    return fetch(`${BASE_URL}/recipes/`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        }
    })
    .then(handleResponse);
};

export const getRecipe = (id, token) => {
    return fetch(`${BASE_URL}/recipes/${id}/`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token ? `Bearer ${token}` : ''
        }
    })
    .then(handleResponse);
};

export const createRecipe = (data, token) => {
    return fetch(`${BASE_URL}/recipes/`, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(handleResponse);
};

export const updateRecipe = (id, data, token) => {
    return fetch(`${BASE_URL}/recipes/${id}/`, {
        method: 'PATCH',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(data)
    })
    .then(handleResponse);
};

export const deleteRecipe = (id, token) => {
    return fetch(`${BASE_URL}/recipes/${id}/`, {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    })
    .then(handleResponse);
};

export const getIngredients = () => {
    return fetch(`${BASE_URL}/ingredients/`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(handleResponse);
};

export const getTags = () => {
    return fetch(`${BASE_URL}/tags/`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
    .then(handleResponse);
}; 