"""Mundo 9 · Cuartel Ciber (cierre del año): lo que Pinion casi no toca y a esta edad urge: huella digital,
contraseñas, estafas y phishing, desinformación y videos falsos, ciberacoso y tiempo de pantalla. Termina con el
portafolio del año, un pitch de 60 segundos y el jefe final."""
from .base import CARPETA, clasifica, jefe, leccion, mision

JUEGOS = {
    'clasifica_publicar': clasifica('¿Lo publicarías?', '📱', 'Antes de publicar, piensa: ¿lo vería sin problema mi '
                                    'familia, mi escuela y un desconocido?', [
        ('Sin problema', '👍', ['Un dibujo o un proyecto que hiciste', 'Tu opinión respetuosa sobre una película',
                                'Una foto del paisaje de tus vacaciones, ya de regreso',
                                'Tu récord en el juego de la clase', 'Una receta que te salió muy bien']),
        ('Lo pienso dos veces', '🤔', ['Una foto donde sale un amigo (primero pide permiso)',
                                       'Un video de una fiesta de cumpleaños', 'Un comentario cuando estás muy enojado',
                                       'Una foto con el uniforme de tu escuela', 'Un chiste sobre alguien del salón']),
        ('Nunca', '⛔', ['Tu contraseña', 'Tu dirección o tu ubicación en tiempo real', 'Tu número de teléfono',
                         'Fotos de otras personas sin su permiso', 'La captura de un chat privado de alguien',
                         'Los datos de la tarjeta de tus papás']),
    ], rondas=14),
    'clasifica_estafa': clasifica('¿Estafa o legítimo?', '🎣', 'Las estafas usan prisa, premios increíbles y enlaces '
                                  'raros. ¿Cuál es cuál?', [
        ('Estafa', '🎣', ['¡Ganaste 10,000 Robux! Escribe tu contraseña aquí',
                          'Tu cuenta se cerrará en 24 horas: verifica tus datos ya',
                          'Un generador de monedas gratis para tu juego',
                          'Un desconocido te pide el código que te llegó por SMS',
                          'Un correo de «Netfl1x» pide actualizar tu tarjeta',
                          'Un jugador te ofrece skins si sales del juego a otra app']),
        ('Legítimo', '✅', ['Tu profe comparte el enlace de MakeCode en la plataforma de clase',
                            'La app oficial te pide actualizarse desde la tienda de apps',
                            'Escribes tú la dirección del banco en el navegador',
                            'Un aviso dentro del juego oficial que no pide datos',
                            'Un correo de la escuela con el horario y sin enlaces raros',
                            'Tu familia te pide activar la verificación en dos pasos']),
    ], rondas=12),
}

MUNDO = {
    'nombre': 'Cuartel Ciber', 'tema': 'cyber',
    'descripcion': 'Cierre del año. Ya sabes crear videojuegos, documentos, modelos 3D y contenido con IA. Ahora toca '
                   'protegerte: huella digital, contraseñas, estafas, noticias falsas y convivencia en línea. Al final, '
                   'arma tu portafolio, presenta tu mejor proyecto en 60 segundos y enfrenta al jefe final.',
    'niveles': [
        {'nombre': 'Identidad digital', 'cofre': 30, 'misiones': [
            mision('Tu huella digital', 'texto', leccion(
                intro='Cada cosa que publicas, comentas, compartes o buscas deja un rastro: tu huella digital. Y en '
                      'internet casi nada se borra de verdad.',
                saber=['Huella digital: todo lo que se puede saber de ti por lo que hay en internet.',
                       'Huella activa: lo que publicas tú. Huella pasiva: lo que las apps registran de ti (ubicación, '
                       'búsquedas, lo que ves y cuánto tiempo).',
                       'Una captura de pantalla puede guardar para siempre algo que tú borraste.'],
                pasos=['Haz la lista de las apps o juegos donde tienes cuenta (o usas la de alguien de tu familia).',
                       '¿Qué información tuya podría encontrar alguien ahí? (foto, nombre, escuela, ubicación…)',
                       '¿Hay algo que hayas publicado o enviado que no te gustaría que viera tu futura secundaria?',
                       'Escribe 2 acciones para cuidar tu huella desde hoy.'],
                entrega='escribe tus respuestas aquí abajo. Nadie más que tu profe las verá.'), xp=60),
            mision('Huella y privacidad', 'cuestionario', leccion(
                intro='Cuidar tu privacidad no es esconderte: es decidir tú qué se sabe de ti.',
                saber=['La mayoría de las redes sociales piden tener al menos 13 años.',
                       'Configuración de privacidad: decide quién ve tus publicaciones (solo amigos, no «público») y '
                       'apaga la ubicación de las apps que no la necesitan.',
                       'Datos personales que nunca se publican: dirección, teléfono, escuela, ubicación en tiempo real, '
                       'contraseñas.',
                       'Antes de publicar algo de otra persona, se le pide permiso.',
                       'Regla de las 3 personas: si no te gustaría que lo vieran tu familia, tu escuela y un desconocido, '
                       'no lo publiques.']), xp=60, preguntas=[
                ('¿Qué es la huella digital?', 'Todo lo que se puede saber de ti por lo que hay en internet',
                 ['La marca de tu dedo en la pantalla', 'Un tipo de contraseña', 'Un virus']),
                ('¿Cuántos años piden la mayoría de las redes sociales?', 'Al menos 13',
                 ['8', '10', 'No piden edad']),
                ('¿Quién debería ver tus publicaciones?', 'Solo personas que conoces en la vida real',
                 ['Todo el mundo', 'Cualquiera que te siga', 'Desconocidos con muchos seguidores']),
                ('¿Qué haces antes de publicar la foto de un amigo?', 'Le pido permiso',
                 ['La publico y luego le aviso', 'Le pongo un filtro', 'Nada']),
                ('¿Qué es la huella pasiva?', 'Lo que las apps registran de ti sin que lo publiques',
                 ['Lo que publicas a propósito', 'Una foto borrosa', 'Un juego sin internet']),
                ('Borraste una publicación. ¿Desapareció para siempre?', 'No necesariamente: alguien pudo hacer captura',
                 ['Sí, siempre', 'Solo si fue de noche', 'Sí, si tenía pocos likes']),
            ]),
            mision('Contraseñas de nivel pro', 'texto', leccion(
                intro='Una contraseña débil se adivina en segundos. Aprende el método que usan los expertos.',
                saber=['Más larga es más fuerte: mínimo 12 caracteres.',
                       'Frase de contraseña: 3 o 4 palabras al azar que no tengan relación entre sí, con un número y un '
                       'símbolo. Fácil de recordar, difícil de adivinar.',
                       'Nunca uses tu nombre, tu cumpleaños, el nombre de tu mascota ni tu equipo favorito.',
                       'Una contraseña distinta para cada cuenta importante.',
                       'Verificación en dos pasos: además de la contraseña, te piden un código en el celular.',
                       'Tu contraseña y tus códigos no se comparten, ni con tu mejor amigo. Solo con tu familia.',
                       'En computadoras compartidas (como las de la escuela) siempre cierra sesión.'],
                pasos=['Inventa un EJEMPLO de frase de contraseña con el método (¡no la uses de verdad!).',
                       'Explica por qué es más segura que «juan2014».',
                       'Escribe 3 contraseñas malas que la gente usa y por qué son malas.',
                       'Pregunta en casa si tienen activada la verificación en dos pasos en el correo.'],
                ojo=['Nunca escribas aquí ni en ningún lado una contraseña que de verdad uses.'],
                entrega='escribe tu ejemplo y tus respuestas aquí abajo.'), xp=60),
            mision('¿Lo publicarías?', 'juego', leccion(
                intro='Decide qué se puede publicar, qué hay que pensar dos veces y qué nunca se publica.'),
                juego='clasifica_publicar'),
        ]},
        {'nombre': 'Modo anti-estafas', 'cofre': 30, 'misiones': [
            mision('Detecta el phishing', 'cuestionario', leccion(
                intro='Phishing (se pronuncia «fishing», como pescar): mensajes falsos que te «pescan» para robarte '
                      'contraseñas, cuentas o dinero. En los videojuegos están por todos lados.',
                saber=['Señales de alerta: prisa («¡solo 24 horas!»), premios increíbles (monedas o skins gratis), '
                       'remitentes o enlaces con letras cambiadas («rob1ox»), te piden contraseña o un código, faltas de '
                       'ortografía.',
                       'Los generadores de monedas gratis NO existen: son trampas para robar cuentas.',
                       'Qué hacer: no hagas clic, no respondas, toma captura, avisa a un adulto, bloquea y reporta.',
                       'Si quieres revisar tu cuenta, escribe tú la dirección oficial en el navegador; no uses el enlace '
                       'del mensaje.']), xp=60, preguntas=[
                ('¿Qué es el phishing?', 'Mensajes falsos para robarte contraseñas o cuentas',
                 ['Un juego de pesca', 'Una red social nueva', 'Un antivirus']),
                ('Te llega: «¡Ganaste 10,000 Robux! Escribe tu contraseña». ¿Qué es?', 'Una estafa',
                 ['Un regalo real', 'Un mensaje de la escuela', 'Una actualización']),
                ('¿Cuál es una señal de alerta?', 'Te meten prisa: «solo tienes 24 horas»',
                 ['El mensaje es de tu profe en clase', 'No pide nada', 'Viene en la app oficial sin enlaces']),
                ('El enlace dice «rob1ox.com». ¿Qué notas?', 'Tiene un número en lugar de una letra: es falso',
                 ['Nada raro', 'Es la versión nueva', 'Es más rápido']),
                ('Te llegó un mensaje sospechoso. ¿Qué haces?', 'No hago clic, aviso a un adulto y lo reporto',
                 ['Hago clic para ver qué pasa', 'Lo reenvío a mis amigos', 'Respondo con mis datos']),
                ('¿Existen los generadores de monedas gratis para juegos?', 'No, son trampas para robar cuentas',
                 ['Sí, todos funcionan', 'Solo los fines de semana', 'Sí, si tienes muchos amigos']),
            ]),
            mision('¿Estafa o legítimo?', 'juego', leccion(
                intro='Revisa cada mensaje como un experto en ciberseguridad: ¿te meten prisa, te prometen algo '
                      'increíble o te piden datos?',
                tip='Un mensaje legítimo nunca te pide tu contraseña ni el código que te llegó por SMS.'),
                juego='clasifica_estafa'),
            mision('¿Real o fabricado?', 'cuestionario', leccion(
                intro='Con la IA es fácil fabricar fotos, audios y videos falsos. No siempre se nota a simple vista, así '
                      'que lo importante es verificar.',
                saber=['Desinformación: información falsa que se comparte como si fuera cierta.',
                       'Video falso (deepfake): un video o audio hecho con IA donde alguien parece decir o hacer algo que '
                       'nunca hizo.',
                       'Lectura lateral: abre otras pestañas y busca qué dicen otras fuentes confiables sobre lo mismo.',
                       'Búsqueda inversa de imágenes: clic derecho en la imagen → «Buscar imagen con Google» (Google '
                       'Lens) para ver de dónde salió.',
                       'Si algo te da mucho enojo, miedo o emoción, sospecha: así se diseñan los contenidos falsos para '
                       'que los compartas sin pensar.']), xp=60, preguntas=[
                ('¿Qué es un deepfake?', 'Un video o audio falso hecho con IA',
                 ['Un video muy largo', 'Una foto borrosa', 'Un juego de miedo']),
                ('¿Qué es la lectura lateral?', 'Buscar en otras fuentes qué dicen sobre lo mismo',
                 ['Leer de lado', 'Leer solo los comentarios', 'Leer muy rápido']),
                ('¿Para qué sirve la búsqueda inversa de imágenes?', 'Para saber de dónde salió una imagen',
                 ['Para voltear la imagen', 'Para borrar la imagen', 'Para hacerla más grande']),
                ('Un video te da muchísimo enojo y quieres compartirlo ya. ¿Qué haces?', 'Hago una pausa y lo verifico',
                 ['Lo comparto rápido', 'Lo comento con groserías', 'Lo mando a todos mis grupos']),
                ('¿Cuál es la mejor defensa contra los videos falsos?', 'Verificar la fuente antes de creer o compartir',
                 ['Buscar errores en las manos', 'Creerle a quien tenga más seguidores', 'No ver videos nunca']),
            ]),
        ]},
        {'nombre': 'Convivencia digital', 'cofre': 35, 'misiones': [
            mision('Ciberacoso: qué hacer', 'cuestionario', leccion(
                intro='Detrás de cada pantalla hay una persona. El ciberacoso lastima de verdad, y todos podemos '
                      'detenerlo.',
                saber=['Ciberacoso: molestar, humillar o excluir a alguien de forma repetida por medios digitales '
                       '(mensajes, memes, grupos, cuentas falsas, fotos sin permiso).',
                       'Si te pasa: no respondas, guarda evidencia (capturas), bloquea, reporta y cuéntale a un adulto de '
                       'confianza.',
                       'Si lo ves: no reenvíes ni des «me gusta», apoya a la persona y avisa a un adulto. Quien se ríe o '
                       'comparte también participa.',
                       'Si alguien que no conoces te pide fotos, datos o que guardes un secreto: deja de responder y '
                       'avísale a un adulto de inmediato.']), xp=60, preguntas=[
                ('¿Qué es el ciberacoso?', 'Molestar o humillar a alguien de forma repetida por medios digitales',
                 ['Jugar en línea con amigos', 'Mandar un mensaje de cumpleaños', 'Discutir una vez']),
                ('Si alguien te acosa en línea, ¿qué haces primero?', 'No respondo y guardo capturas como evidencia',
                 ['Le respondo con insultos', 'Borro todo', 'Lo publico para que todos lo vean']),
                ('Ves un meme que se burla de un compañero. ¿Qué haces?', 'No lo comparto, apoyo al compañero y aviso',
                 ['Le doy «me gusta»', 'Lo reenvío a otro grupo', 'Le agrego un comentario chistoso']),
                ('Un desconocido te pide fotos y que no le digas a nadie. ¿Qué haces?',
                 'Dejo de responder y le aviso a un adulto de inmediato', ['Le mando una foto', 'Lo guardo en secreto',
                                                                         'Le pido su número']),
                ('¿Por qué es importante guardar capturas?', 'Son evidencia para reportar',
                 ['Para presumir', 'Para subirlas a redes', 'No sirven de nada']),
            ]),
            mision('Cuatro esquinas', 'presencial', leccion(
                intro='Una dinámica en movimiento: cada esquina del salón es una respuesta. Tú decides a dónde ir… y lo '
                      'defiendes con argumentos.',
                dinamica=['El profe lee una situación y las 4 opciones; cada esquina es una opción (A, B, C, D).',
                          'Tienen 10 segundos para caminar (no correr) a su esquina, sin hablar.',
                          'Ya en la esquina, en pareja con quien tengas al lado, preparan un argumento en 30 segundos y '
                          'en voz baja.',
                          'El profe elige a una persona de cada esquina para explicar por qué la eligieron.',
                          'Se vale cambiar de esquina si un argumento te convence.'],
                pasos=['Situación 1: en el grupo del salón comparten un meme que se burla de un compañero.',
                       'Situación 2: un jugador en línea te ofrece skins si le das tu contraseña.',
                       'Situación 3: tu mejor amigo te pide tu contraseña para jugar en tu cuenta.',
                       'Situación 4: te llega un video de un famoso diciendo algo increíble.',
                       'Situación 5: alguien que no conoces te escribe todos los días y te pide guardar el secreto.',
                       'Al final, el grupo escribe en el pizarrón la mejor respuesta de cada situación.'],
                logro=['Defendiste tu decisión con un argumento y conoces la mejor respuesta de cada situación.']), xp=60),
            mision('Mi tiempo de pantalla', 'texto', leccion(
                intro='Muchas apps están diseñadas para que no las sueltes (¿te acuerdas del Scroll Infinito?). Revisa '
                      'tus datos y decide tú.',
                saber=['En el celular: Ajustes → Bienestar digital (Android) o Ajustes → Tiempo en pantalla (iPhone).',
                       'Ahí ves cuántas horas usaste cada app y cuántas veces desbloqueaste el teléfono.',
                       'Trucos que funcionan: quitar notificaciones, poner límites a una app, nada de pantallas una hora '
                       'antes de dormir.'],
                pasos=['En casa, con permiso de tu familia, revisa el tiempo en pantalla de la última semana (tuyo o del '
                       'dispositivo que usas).',
                       '¿Cuántas horas al día en promedio? ¿Qué app ganó?',
                       '¿Te sorprendió? ¿Por qué?',
                       'Escribe una meta concreta para la próxima semana. Ejemplo: «Máximo 1 hora de videos entre semana».'],
                entrega='escribe tus datos y tu meta aquí abajo.'), xp=60),
        ]},
        {'nombre': 'Demo Day', 'cofre': 40, 'misiones': [
            mision('Portafolio del año', 'evidencia', leccion(
                intro='Un portafolio reúne tus mejores trabajos para mostrar de qué eres capaz. Te servirá en la '
                      'secundaria.',
                saber=[f'Organiza tu carpeta {CARPETA} con subcarpetas: 1_Juegos, 2_Documentos, 3_Modelos3D, 4_IA_y_Museo.',
                       'Para los juegos de MakeCode guarda el enlace compartido en un documento; para Tinkercad, una '
                       'captura.',
                       'Elige calidad, no cantidad: tus 3 mejores trabajos.'],
                pasos=['Ordena tus archivos en las 4 subcarpetas.',
                       'Crea una presentación: Portafolio_TuNombre.',
                       'Diapositiva 1: portada con tu nombre, grupo y una frase que te describa.',
                       'Diapositivas 2 a 4: un trabajo por diapositiva con captura, qué aprendiste y el enlace (si tiene).',
                       'Diapositiva 5: lo que más te costó y cómo lo resolviste.',
                       'Diapositiva 6: una meta de tecnología para la secundaria.'],
                logro=['Tu carpeta está ordenada y tu portafolio tiene 6 diapositivas con 3 trabajos y sus enlaces.'],
                entrega='sube una captura de tu carpeta ordenada y de tu portafolio.'), xp=120, monedas=35),
            mision('Pitch de 60 segundos', 'presencial', leccion(
                intro='En el mundo de las startups, un «pitch» es presentar tu idea en un minuto. Hoy presentas tu mejor '
                      'proyecto del año.',
                saber=['Estructura: gancho (una pregunta o un dato) → qué hiciste → con qué herramienta → qué aprendiste '
                       '→ cierre.',
                       'Habla al público, no a la pantalla. Una sola diapositiva de apoyo.'],
                dinamica=['60 segundos exactos con cronómetro visible. Al sonar la alarma, se termina.',
                          'Orden por sorteo. El público escucha en silencio y aplaude al final de cada pitch.',
                          'Cada alumno del público califica 2 pitches con estrellas del 1 al 3.'],
                pasos=['Prepara tu pitch con la estructura (puedes escribirlo en una tarjeta).',
                       'Ensaya con un compañero y cronométrense.',
                       'Preséntalo frente al grupo.',
                       'Escucha la retroalimentación y anota una cosa que harías diferente.'],
                logro=['Presentaste en 60 segundos con gancho, herramienta y aprendizaje.']), xp=60),
            jefe('Jefe final: El Hacker Fantasma', leccion(
                intro='El Hacker Fantasma conoce cada truco digital… pero tú pasaste un año entero entrenando. Este es '
                      'el examen final de TIC 6°.',
                tip='Repasa mecánicas y MakeCode, documentos, hoja de cálculo, 3D, IA y ciberseguridad.'), [
                ('«Los jugadores ahorran para comprar la mejora grande» es…', 'Una dinámica',
                 ['Una mecánica', 'Un sprite', 'Un bug']),
                ('En MakeCode Arcade, ¿qué hace «cambiar porClic a 1»?', 'Le suma 1 a la variable porClic',
                 ['Pone porClic en 1', 'Borra la variable', 'Termina el juego']),
                ('¿Qué herramienta del documento crea el índice automático?', 'Los estilos de título',
                 ['Las notas al pie', 'El zoom', 'El corrector']),
                ('¿Qué fórmula calcula el promedio de B2 a B30?', '=PROMEDIO(B2:B30)',
                 ['=MAX(B2:B30)', '=B2+B30', 'PROMEDIO B2 B30']),
                ('En Tinkercad, ¿qué eje es la altura?', 'Z', ['X', 'Y', 'Ninguno']),
                ('¿Cuánta agua da 1 mm de lluvia en 1 m² de techo?', '1 litro', ['1 mililitro', '10 litros',
                                                                                 '100 litros']),
                ('¿Cuál es la fórmula de un prompt claro?', 'Rol + Tarea + Contexto + Formato + Límites',
                 ['Escribir una sola palabra', 'Todo en mayúsculas', 'Copiar el prompt de otro']),
                ('«Tras revisar todas las pruebas: es un traje de buceo» es…', 'Una conclusión',
                 ['Una inferencia', 'Un prompt', 'Una mecánica']),
                ('¿Cuál es la contraseña más segura?', 'Taco-Nube-Violín-47! (una frase larga al azar)',
                 ['juan2014', '123456', 'micontraseña']),
                ('Te ofrecen monedas gratis si das tu contraseña. ¿Qué es?', 'Phishing: una estafa',
                 ['Un regalo del juego', 'Una actualización', 'Un concurso de la escuela']),
            ], xp=200, monedas=80),
        ]},
    ],
}
