# Taller 4 — Frontend Conversacional

---

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/ddfc8cfc-874e-498e-af3c-59d06d0a4e48" />


# FASE 1. INTRODUCCIÓN AL FRONTEND CONVERSACIONAL

---

## 1.1 Objetivo de la Fase

En este taller se construirá el frontend conversacional de ScrumDev AI utilizando Next.js. El objetivo es desarrollar la interfaz mediante la cual el humano podrá interactuar con los agentes IA, visualizar workflows, monitorear procesos y aprobar decisiones críticas del sistema.

El frontend actuará como la capa de interacción humano ↔ plataforma, mientras que toda la lógica de negocio continuará ejecutándose en los microservicios backend construidos en talleres anteriores.

---

## 1.2 Comprender la Arquitectura Frontend

El frontend no ejecutará agentes directamente. Su responsabilidad será:

```text
capturar mensajes humanos
visualizar respuestas agentes
mostrar estados workflows
gestionar autenticación
mostrar trazabilidad
consumir APIs backend
```

Arquitectura conceptual:

```text
Humano
→ Frontend Next.js
→ API Gateway
→ Backend Services
→ Temporal
→ Agents
```

---

# FASE 2. CREACIÓN DEL PROYECTO NEXT.JS

---

## 2.1 Objetivo de la Fase

En esta fase se inicializará el proyecto frontend utilizando Next.js, TypeScript y TailwindCSS.

---

## 2.2 Crear Proyecto Frontend

Desde la raíz del proyecto ejecutar:

```bash
npx create-next-app@latest frontend/web-chat
```

Configurar:

```text
TypeScript → Yes
ESLint → Yes
TailwindCSS → Yes
src/ directory → Yes
App Router → Yes
Turbopack → Yes
```

---

## 2.3 Ingresar al Proyecto Frontend

Ejecutar:

```bash
cd frontend/web-chat
```

---

## 2.4 Ejecutar Proyecto

Ejecutar:

```bash
npm run dev
```

Abrir:

```text
http://localhost:3000
```

Resultado esperado:

```text
pantalla inicial Next.js
```

---

# FASE 3. CONFIGURACIÓN DEL FRONTEND

---

## 3.1 Objetivo de la Fase

El frontend necesita conectarse al backend distribuido utilizando variables de entorno desacopladas.

---

## 3.2 Crear Archivo `.env.local`

Crear archivo:

```bash
touch .env.local
```

Agregar:

```env
NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8080
NEXT_PUBLIC_WS_URL=ws://localhost:8080/ws
NEXT_PUBLIC_APP_NAME=ScrumDev AI
```

---

## 3.3 Comprender Variables `NEXT_PUBLIC`

En Next.js las variables públicas deben comenzar con:

```text
NEXT_PUBLIC_
```

para que puedan ser utilizadas desde el navegador.

---

# FASE 4. ORGANIZACIÓN DEL FRONTEND

---

## 4.1 Objetivo de la Fase

El frontend debe organizarse modularmente para facilitar mantenibilidad y escalabilidad.

---

## 4.2 Crear Estructura Frontend

Ejecutar:

```bash
mkdir -p src/components/chat
mkdir -p src/components/layout
mkdir -p src/components/workflows
mkdir -p src/components/agents
mkdir -p src/components/forms
mkdir -p src/lib/api
mkdir -p src/lib/ws
mkdir -p src/types
mkdir -p src/hooks
mkdir -p src/store
mkdir -p src/styles
```

---

## 4.3 Comprender la Separación Modular

| Carpeta | Responsabilidad |
|---|---|
| `components/chat` | Chat conversacional |
| `components/workflows` | Visualización workflows |
| `components/agents` | Estado agentes |
| `lib/api` | Cliente HTTP |
| `lib/ws` | WebSockets |
| `hooks` | Hooks reutilizables |
| `store` | Estado global |

---

# FASE 5. CONFIGURACIÓN DEL CLIENTE API

---

## 5.1 Objetivo de la Fase

El frontend debe consumir APIs backend mediante un cliente HTTP centralizado.

---

## 5.2 Instalar Axios

Ejecutar:

```bash
npm install axios
```

---

## 5.3 Crear Cliente HTTP

Crear archivo:

```bash
touch src/lib/api/client.ts
```

Agregar:

```typescript
import axios from "axios";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_GATEWAY_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
```

---

## 5.4 Comprender el Cliente Centralizado

Centralizar el cliente permite:

```text
reutilización
interceptores
manejo errores
autenticación
logging
```

---

# FASE 6. CREACIÓN DEL CHAT CONVERSACIONAL

---

## 6.1 Objetivo de la Fase

El chat será el principal mecanismo de interacción humano ↔ ScrumDev AI.

---

## 6.2 Crear Tipos del Chat

Crear archivo:

```bash
touch src/types/chat.ts
```

Agregar:

```typescript
export interface ChatMessage {
  id: string;
  role: "human" | "agent";
  content: string;
  timestamp: string;
}
```

---

## 6.3 Crear Componente ChatMessage

Crear archivo:

```bash
touch src/components/chat/chat-message.tsx
```

Agregar:

```tsx
import { ChatMessage } from "@/types/chat";

interface Props {
  message: ChatMessage;
}

export function ChatMessageItem({ message }: Props) {
  return (
    <div className="border rounded p-3 mb-2">
      <strong>{message.role}</strong>
      <p>{message.content}</p>
    </div>
  );
}
```

---

## 6.4 Crear Componente ChatWindow

Crear archivo:

```bash
touch src/components/chat/chat-window.tsx
```

Agregar:

```tsx
"use client";

import { useState } from "react";

import { ChatMessageItem } from "./chat-message";

export function ChatWindow() {

  const [messages, setMessages] = useState([]);

  return (
    <div className="p-4">
      {messages.map((message: any) => (
        <ChatMessageItem
          key={message.id}
          message={message}
        />
      ))}
    </div>
  );
}
```

---

## 6.5 Crear Componente ChatInput

Crear archivo:

```bash
touch src/components/chat/chat-input.tsx
```

Agregar:

```tsx
"use client";

import { useState } from "react";

export function ChatInput() {

  const [message, setMessage] = useState("");

  return (
    <div className="flex gap-2 mt-4">
      <input
        className="border p-2 flex-1"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <button className="border px-4">
        Enviar
      </button>
    </div>
  );
}
```

---

# FASE 7. CONEXIÓN CHAT ↔ BACKEND

---

## 7.1 Objetivo de la Fase

El frontend debe enviar mensajes al Conversation Service mediante el API Gateway.

---

## 7.2 Crear Servicio Conversacional

Crear archivo:

```bash
touch src/lib/api/conversation-api.ts
```

Agregar:

```typescript
import { apiClient } from "./client";

export async function sendMessage(content: string) {

  const response = await apiClient.post(
    "/messages",
    {
      user_id: "u1",
      project_key: "SDAI",
      content
    }
  );

  return response.data;
}
```

---

## 7.3 Integrar ChatInput

Editar:

```text
src/components/chat/chat-input.tsx
```

Agregar:

```tsx
import { sendMessage } from "@/lib/api/conversation-api";
```

Modificar botón:

```tsx
<button
  className="border px-4"
  onClick={async () => {
    await sendMessage(message);
    setMessage("");
  }}
>
  Enviar
</button>
```

---

# FASE 8. WEBSOCKETS Y TIEMPO REAL

---

## 8.1 Objetivo de la Fase

El frontend debe recibir eventos y respuestas de agentes en tiempo real.

---

## 8.2 Crear Cliente WebSocket

Crear archivo:

```bash
touch src/lib/ws/socket.ts
```

Agregar:

```typescript
export function createSocket() {

  return new WebSocket(
    process.env.NEXT_PUBLIC_WS_URL!
  );
}
```

---

## 8.3 Comprender Tiempo Real

WebSockets permitirán:

```text
streaming respuestas
eventos workflows
actualización agentes
notificaciones
```

---

# FASE 9. PANEL DE WORKFLOWS

---

## 9.1 Objetivo de la Fase

El usuario debe visualizar workflows ejecutándose dentro de Temporal.

---

## 9.2 Crear Componente WorkflowCard

Crear archivo:

```bash
touch src/components/workflows/workflow-card.tsx
```

Agregar:

```tsx
interface Props {
  workflowId: string;
  status: string;
}

export function WorkflowCard({
  workflowId,
  status
}: Props) {

  return (
    <div className="border rounded p-4">
      <h3>{workflowId}</h3>
      <p>{status}</p>
    </div>
  );
}
```

---

## 9.3 Comprender Visualización Workflows

El frontend mostrará:

```text
estado workflows
agentes activos
errores
aprobaciones pendientes
eventos
```

---

# FASE 10. PANEL DE AGENTES

---

## 10.1 Objetivo de la Fase

El usuario debe visualizar qué agentes están trabajando y sus responsabilidades.

---

## 10.2 Crear AgentCard

Crear archivo:

```bash
touch src/components/agents/agent-card.tsx
```

Agregar:

```tsx
interface Props {
  name: string;
  role: string;
  status: string;
}

export function AgentCard({
  name,
  role,
  status
}: Props) {

  return (
    <div className="border rounded p-4">
      <h3>{name}</h3>
      <p>{role}</p>
      <span>{status}</span>
    </div>
  );
}
```

---

## 10.3 Comprender Observabilidad de Agentes

La interfaz permitirá visualizar:

```text
agentes activos
estado ejecución
decisiones
workflow actual
```

---

# FASE 11. FORMULARIO DE REQUERIMIENTOS NO FUNCIONALES

---

## 11.1 Objetivo de la Fase

El frontend permitirá capturar requerimientos no funcionales antes de iniciar generación arquitectónica.

---

## 11.2 Crear Formulario NFR

Crear archivo:

```bash
touch src/components/forms/nfr-form.tsx
```

Agregar:

```tsx
"use client";

export function NFRForm() {

  return (
    <form className="space-y-4">

      <label>
        Escalabilidad requerida
      </label>

      <select className="border p-2 w-full">
        <option>Alta</option>
        <option>Media</option>
        <option>Baja</option>
      </select>

      <label>
        ¿Requiere alta disponibilidad?
      </label>

      <input type="checkbox" />

    </form>
  );
}
```

---

## 11.3 Comprender los NFR

Los requerimientos no funcionales permitirán que los agentes:

```text
seleccionen arquitectura
apliquen patrones
definan escalabilidad
determinen seguridad
```

---

# FASE 12. ESTADO GLOBAL FRONTEND

---

## 12.1 Objetivo de la Fase

El frontend necesita un estado global para compartir información entre componentes.

---

## 12.2 Instalar Zustand

Ejecutar:

```bash
npm install zustand
```

---

## 12.3 Crear Store Global

Crear archivo:

```bash
touch src/store/chat-store.ts
```

Agregar:

```typescript
import { create } from "zustand";

interface ChatStore {

  messages: any[];

  setMessages: (
    messages: any[]
  ) => void;
}

export const useChatStore = create<ChatStore>(
  (set) => ({

    messages: [],

    setMessages: (messages) =>
      set({ messages }),
  })
);
```

---

# FASE 13. DASHBOARD PRINCIPAL

---

## 13.1 Objetivo de la Fase

La aplicación necesita un dashboard centralizado para integrar chat, workflows y agentes.

---

## 13.2 Crear Dashboard

Editar:

```text
src/app/page.tsx
```

Agregar:

```tsx
import { ChatWindow } from "@/components/chat/chat-window";
import { ChatInput } from "@/components/chat/chat-input";

export default function HomePage() {

  return (
    <main className="p-6">

      <h1 className="text-3xl font-bold mb-6">
        ScrumDev AI
      </h1>

      <ChatWindow />

      <ChatInput />

    </main>
  );
}
```

---

## 13.3 Ejecutar Frontend

Ejecutar:

```bash
npm run dev
```

Abrir:

```text
http://localhost:3000
```

---

# FASE 14. VALIDACIÓN FINAL

---

## 14.1 Objetivo de la Fase

Validar funcionamiento completo del frontend conversacional.

---

## 14.2 Verificar Frontend

Verificar:

```text
Next.js ejecutando
chat visible
formulario NFR visible
componentes cargando
conexión backend funcionando
```

---

## 14.3 Resultado Esperado

Al finalizar este taller el estudiante tendrá:

```text
frontend Next.js funcionando
chat conversacional implementado
cliente API configurado
WebSockets preparados
dashboard inicial construido
panel workflows creado
panel agentes creado
formulario NFR implementado
estado global configurado
frontend conectado backend
```

El sistema quedará preparado para integrar todos los componentes y ejecutar pruebas end-to-end en el siguiente taller.
