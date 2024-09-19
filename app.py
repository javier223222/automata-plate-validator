from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

class PlacaEvaluatorDFA:
    def __init__(self):
        self.state = 'q0'  # Estado inicial
        self.final_states = {'q9', 'q15', 'q23', 'q31', 'q36'}  # Estados de aceptación

    def is_valid_letter(self, char):
        """Valida que el carácter sea una letra permitida."""
        return char.isalpha() and char not in {'I', 'O', 'Q'}  # Letras no permitidas

    def is_valid_number(self, char):
        """Valida que el carácter sea un número."""
        return char.isdigit()

    def transition(self, current_state, char):
        """
        Función de transición optimizada para manejar todos los tipos de placas.
        """
        # Estado inicial q0
        if current_state == 'q0':
            if self.is_valid_letter(char):
                
                return 'q1'  # Letra inicial Automóvil/Camión/Placa Policiaca
            elif self.is_valid_number(char):
                return 'q15'  # Primer número Autobús privado

        # Automóviles privados (LLL-NNN-L)
        elif current_state == 'q1':
            if self.is_valid_letter(char):
                return 'q2'  # Segunda letra
            elif char == '-':
                return "q24"
        elif current_state == 'q2':
            
            if self.is_valid_letter(char):
                return 'q3'  # Tercera letra Automóvil
            elif char == '-':
                return 'q10'
            
        elif current_state == 'q3':

            if char == '-':
                
                
                return 'q4'  # Guion
        elif current_state == 'q4':
            if self.is_valid_number(char):
                return 'q5'  # Primer número Automóvil
        elif current_state == 'q5':
            if self.is_valid_number(char):
                return 'q6'  # Segundo número
        elif current_state == 'q6':
            if self.is_valid_number(char):
                return 'q7'  # Tercer número
        elif current_state == 'q7':
            if char == '-':
                return 'q8'  # Segundo guion
        elif current_state == 'q8':
            if self.is_valid_letter(char):
                
                return 'q9'  # Letra final Automóvil
               

        
        elif current_state == 'q10':
            if self.is_valid_number(char):
                return 'q11'  # Primer número Camión
        elif current_state == 'q11':
            if self.is_valid_number(char):
                return 'q12'  # Segundo número
        elif current_state == 'q12':
            if self.is_valid_number(char):
                return 'q13'  # Tercer número
        elif current_state == 'q13':
            if self.is_valid_number(char):
                return 'q14'  # Cuarto número
            elif self.is_valid_letter(char):
                return 'q36'
        elif current_state == 'q14':
            if char == '-':
                return 'q8'  # Segundo guion (reutilizamos la transición para la letra final)
        elif current_state == 'q8':
            if self.is_valid_letter(char):
                return 'q9'  # Letra final Camión

        # Autobuses privados (NN-LLL-NN)
        elif current_state == 'q15':
            if self.is_valid_number(char):
                return 'q16'  # Segundo número
        elif current_state == 'q16':
            if char == '-':
                return 'q17'  # Guion
        elif current_state == 'q17':
            if self.is_valid_letter(char):
                return 'q18'  # Primera letra Autobús privado
        elif current_state == 'q18':
            if self.is_valid_letter(char):
                return 'q19'  # Segunda letra
        elif current_state == 'q19':
            if self.is_valid_letter(char):
                return 'q20'  # Tercera letra
        elif current_state == 'q20':
            if char == '-':
                return 'q21'  # Segundo guion
        elif current_state == 'q21':
            if self.is_valid_number(char):
                return 'q22'  # Primer número final
        elif current_state == 'q22':
            if self.is_valid_number(char):
                return 'q23'  # Segundo número final

        # Autobuses públicos (Z-999-ZSZ)
      
        elif current_state == 'q24':
            if self.is_valid_number(char):
                return 'q25'  # Primer número
        elif current_state == 'q25':
            if self.is_valid_number(char):
                return 'q26'  # Segundo número
        elif current_state == 'q26':
            if self.is_valid_number(char):
                return 'q27'  # Tercer número
        elif current_state == 'q27':
            if char == '-':
                return 'q28'  # Segundo guion
        elif current_state == 'q28':
            if self.is_valid_letter(char):
                return 'q29'  # Primera letra final
        elif current_state == 'q29':
            if self.is_valid_letter(char):
                return 'q30'  # Segunda letra final
        elif current_state == 'q30':
            if self.is_valid_letter(char):
                return 'q31'  # Tercera letra final

        # Placas policiacas (LL-NNNL-L)
        elif current_state == 'q1':
            if char == '-':
                return 'q32'  # Guion Placas Policiacas
        elif current_state == 'q32':
            if self.is_valid_number(char):
                return 'q33'  # Primer número
        elif current_state == 'q33':
            if self.is_valid_number(char):
                return 'q34'  # Segundo número
        elif current_state == 'q34':
            if self.is_valid_number(char):
                return 'q35'  # Tercer número
        elif current_state == 'q35':
            if self.is_valid_letter(char):
                return 'q36'  # Letra intermedia
        elif current_state == 'q36':
            if char == '-':
                return 'q8'  # Segundo guion (reutilizamos el guion final)
        elif current_state == 'q8':
            if self.is_valid_letter(char):
                return 'q9'  # Letra final

        return 'invalid'

    def evaluate_plate(self, plate):
        """
        Evalúa la placa utilizando el DFA.
        """
        
        self.state = 'q0'  # Estado inicial
        for char in plate:
            print(char)
            print(self.transition(self.state, char))
            self.state = self.transition(self.state, char)
            if self.state == 'invalid':
                return False
        
        return self.state in self.final_states  # Acepta si está en un estado final


# Lógica para evaluar el texto con las placas
class PlacaEvaluator:
    @staticmethod
    def evaluate_text(text):
        dfa = PlacaEvaluatorDFA()
        posibles_placas = text.split()
        print(posibles_placas)
        results = {}
        for placa in posibles_placas:
            print(placa)
            if dfa.evaluate_plate(placa):
                results[placa] = "Placa válida"
            else:
                results[placa] = "Placa inválida"
        return results

@app.post("/evaluate-placas/")
async def evaluate_placas(file: UploadFile = File(...)):
    """
    Procesa un archivo subido y evalúa las placas.
    """
    try:
        contents = await file.read()
        text = contents.decode('utf-8')
        result = PlacaEvaluator.evaluate_text(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando el archivo: {str(e)}")

@app.post("/evaluate-placas-text/")
async def evaluate_placas_text(input: TextInput):
    """
    Procesa una cadena de texto y evalúa las placas.
    """
    try:
        print(input.text)
        result = PlacaEvaluator.evaluate_text(input.text)

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando la cadena de texto: {str(e)}")
