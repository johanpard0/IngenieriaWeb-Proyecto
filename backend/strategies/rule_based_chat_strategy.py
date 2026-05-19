import random

class RuleBasedChatStrategy:

    responses = {
        "saludos": [
            "¡Hola! ¿En qué puedo ayudarte?",
            "¡Hola! Soy Catalina, tu asistente virtual.",
            "¡Hola! ¿Cómo puedo asistirte hoy?"
        ],
        "horarios": [
            "Los horarios de los salones están disponibles en el portal de la universidad.",
            "Puedes revisar los horarios en la plataforma académica.",
            "Los horarios de clases se publican en el portal institucional."
        ],
        "salones": [
            "Los salones están distribuidos por bloques. ¿Cuál necesitas?",
            "Puedes consultar los salones por bloque y piso.",
            "¿Qué salón deseas ubicar?"
        ],
        "profesores": [
            "Puedes consultar los profesores por materia.",
            "¿Sobre qué profesor necesitas información?",
            "Dime la materia y te indico el docente."
        ]
    }

    def generate_response(self, message: str) -> str:

        user_message = message.lower()

        if "hola" in user_message or "buenos días" in user_message or "hey" in user_message:
            return random.choice(self.responses["saludos"])

        if "salon" in user_message or "salón" in user_message:

            if "a101" in user_message:
                return "El salón A101 está en el bloque A, primer piso."

            if "b202" in user_message:
                return "El salón B202 está en el bloque B, segundo piso."

            return random.choice(self.responses["salones"])

        if "profesor" in user_message or "quien dicta" in user_message:

            if "bases de datos" in user_message:
                return "Bases de Datos la dicta el profesor Carlos Pérez en el salón A101."

            if "redes" in user_message:
                return "Redes la dicta la profesora Ana Gómez en el salón B202."

            return random.choice(self.responses["profesores"])

        if "horario" in user_message:
            return random.choice(self.responses["horarios"])

        if "perfil" in user_message:
            return "Perfil de usuario: Usuario activo."

        if "configuracion" in user_message or "configuración" in user_message:
            return "Configuración disponible próximamente."

        if "historial" in user_message:
            return "Historial disponible próximamente."

        return "No entendí tu mensaje."