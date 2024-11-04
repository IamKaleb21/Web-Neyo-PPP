// src/pages/Dashboard.tsx
import { useLocation, useNavigate } from 'react-router-dom'
import Button from '../components/Button'

export default function Dashboard() {
  const location = useLocation()
  const navigate = useNavigate()
  const email = location.state?.email || "Usuario"

  const handlePasswordChange = () => {
    // Aquí podrías implementar la lógica para cambiar la contraseña
    // Por simplicidad, mostraremos una alerta
    alert(`Función de cambio de contraseña para ${email}`)
  }

  const handleLogout = () => {
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    navigate("/login")
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md text-center">
        <h1 className="text-2xl font-bold mb-4">Bienvenido, {email}</h1>
        <p className="mb-8">¡Has iniciado sesión correctamente!</p>
        <Button onClick={handlePasswordChange}>Cambiar Contraseña</Button>
        <Button onClick={handleLogout} className="mt-4 bg-red-600 hover:bg-red-700">
          Cerrar sesión
        </Button>
      </div>
    </div>
  )
}
