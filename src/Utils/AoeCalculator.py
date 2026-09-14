from typing import Set, Tuple

class AoECalculator:
    @staticmethod
    def get_linear_cross(startX: int, startY: int, rangeLimit: int, maxCols: int, maxRows: int) -> Set[Tuple[int, int]]:
        area = set()
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Arriba, Abajo, Izquierda, Derecha
        
        for dx, dy in directions:
            for r in range(1, rangeLimit + 1):
                nx = startX + (dx * r)
                ny = startY + (dy * r)
                
                # Respetar los límites lógicos de la matriz
                if 0 <= nx < maxCols and 0 <= ny < maxRows:
                    area.add((nx, ny))
                else:
                    break # Detener la proyección en esta dirección si tocamos el borde
                    
        return area

    @staticmethod
    def get_square_area(centerX: int, centerY: int, radius: int, maxCols: int, maxRows: int) -> Set[Tuple[int, int]]:
        area = set()

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx = centerX + dx
                ny = centerY + dy

                if 0 <= nx < maxCols and 0 <= ny < maxRows:
                    area.add((nx, ny))
                    
        return area