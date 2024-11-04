import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import Input from '../components/Input'
import Button from '../components/Button'

export default function Dashboard() {
  const location = useLocation()
  const navigate = useNavigate()
  const email = location.state?.email || "Usuario"
  const [nuevaContrasena, setNuevaContrasena] = useState('')
  const [confirmarContrasena, setConfirmarContrasena] = useState('')
  const [mensaje, setMensaje] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    navigate("/login")
  }

  const handleActualizarContrasena = async () => {
    setError(null)
    setMensaje(null)
    setLoading(true)

    if (nuevaContrasena !== confirmarContrasena) {
      setError("Las contraseñas no coinciden")
      setLoading(false)
      return
    }

    try {
      const access_token = localStorage.getItem("access_token")
      const response = await fetch("http://localhost:8000/auth/actualizar-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${access_token}`
        },
        body: JSON.stringify({ nueva_contrasena: nuevaContrasena }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        setError(errorData.detail || "Error al actualizar la contraseña")
        return
      }

      const data = await response.json()
      setMensaje(data.message)

    } catch (err) {
      setError("Error de red o servidor")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md text-center">
        <h1 className="text-2xl font-bold mb-4">Bienvenido, {email}</h1>
        <p className="mb-8">¡Has iniciado sesión correctamente!</p>

        {/* Formulario para actualizar la contraseña */}
        <div className="mb-6">
          <Input
            label="Nueva Contraseña"
            type="password"
            value={nuevaContrasena}
            onChange={(e) => setNuevaContrasena(e.target.value)}
          />
          <Input
            label="Confirmar Contraseña"
            type="password"
            value={confirmarContrasena}
            onChange={(e) => setConfirmarContrasena(e.target.value)}
          />
          {mensaje && <p className="text-green-600 text-sm">{mensaje}</p>}
          {error && <p className="text-red-600 text-sm">{error}</p>}
          <Button onClick={handleActualizarContrasena} disabled={loading}>
            {loading ? 'Actualizando...' : 'Actualizar Contraseña'}
          </Button>
        </div>

        <Button onClick={handleLogout} className="bg-red-600 hover:bg-red-700">
          Cerrar sesión
        </Button>
      </div>
    </div>
  )
}
