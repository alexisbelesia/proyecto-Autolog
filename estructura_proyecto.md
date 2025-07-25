# 🧠 ¿Separar todo o agrupar apps en Django?

---

## 🎯 Objetivo de esta decisión

Elegir una estructura que sea:

◆ Escalable: que no colapse si el proyecto crece.  
◆ Mantenible: que sea fácil de entender y modificar.  
◆ Eficiente para trabajar en equipo.

---

## 📊 Comparativa: Separar todo vs. Agrupar un poco

| Criterio                         | Separar TODO (una app por entidad) | Agrupar FUNCIONALIDAD |
|----------------------------------|------------------------------------|------------------------|
| 🔍 Claridad conceptual           | ✅ Máxima claridad por entidad      | ✅ Claridad funcional  |
| 📁 Cantidad de carpetas          | ❌ Muchísimas apps                  | ✅ Menos apps           |
| 🧩 Modularidad                   | ✅ Reutilizable en otros proyectos | ⚠️ A veces limitada     |
| 👥 Trabajo en equipo             | ⚠️ Más coordinación por integración| ✅ Menos fricción       |
| 🧠 Carga cognitiva               | ❌ Más difícil de entender rápido  | ✅ Mejor visión general |
| 🧪 Tests y lógica de negocio     | ✅ Bien encapsulada                 | ✅ También viable       |

---

## ✅ Recomendación: AGRUPAR POR FUNCIONALIDAD

Separar **todo** puede volverse contraproducente salvo que tengas:

✦ Un sistema MUY grande  
✦ Muchas personas trabajando en paralelo  
✦ Apps que querés reutilizar en otros proyectos

En la mayoría de los proyectos universitarios o profesionales en crecimiento, **agrupar lógicamente por funcionalidad** es lo ideal.

---

## 🧱 Propuesta refinada para Autolog

Agrupá en base a **módulos funcionales**, no en base a clases del UML.

### 📦 `vehiculos`
✦ Vehiculo  
✦ Métodos de mantenimiento predictivo

### 📦 `ordenes`
✦ OrdenDeTrabajo  
✦ PracticaMantenimiento  

### 📦`presupuestos`
✦ Presupuesto

### 📦 `talleres`
✦ Taller  
✦ Agenda  
✦ Turnos

### 📦 `usuarios`
✦ Cliente  
✦ PermisoDeAcceso
✦ AdministradorTecnico  
✦ SuperUsuario  
✦ Cualquier futura autenticación/rol

---

## 🧠 Consideración clave

Si algún día `Presupuesto` o `PracticaMantenimiento` crecen mucho y se vuelven **independientes en lógica o visualización**, podés migrarlas a una app propia sin romper nada. Esa es la ventaja de Django.

---

## 🧪 Regla práctica para decidir

> ✦ Si el modelo vive **solo** y tiene lógica propia → considerar app aparte.  
> ✦ Si **depende directamente** de otro modelo → mantenerlo en la misma app.

---
