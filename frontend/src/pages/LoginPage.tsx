// src/pages/LoginPage.tsx
import React, { useState } from 'react'
import Input from '../components/Input'
import Button from '../components/Button'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null) // Reiniciar el mensaje de error antes de cada intento de login

    try {
      // Realizar solicitud al backend usando fetch
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      })

      // Si la respuesta no es exitosa, lanzar un error
      if (!response.ok) {
        const errorData = await response.json()
        setError(errorData.detail || 'Error en el inicio de sesión')
        return
      }

      // Obtener los tokens del backend y almacenarlos en localStorage
      const data = await response.json()
      localStorage.setItem("access_token", data.access_token)
      localStorage.setItem("refresh_token", data.refresh_token)

      // Aquí podrías redirigir al usuario o actualizar el estado de la app
      console.log("Sesión iniciada con éxito")

    } catch (err) {
      setError('Error de red o servidor')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Iniciar sesión en AutoPartes
        </h2>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              label="Correo electrónico"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              error={error}
            />

            <Input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              label="Contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              error={error}
            />

            {error && <p className="text-red-600 text-sm">{error}</p>}

            <Button type="submit" disabled={loading}>
              {loading ? 'Iniciando sesión...' : 'Iniciar sesión'}
            </Button>
          </form>
        </div>
      </div>
    </div>
  )
}
