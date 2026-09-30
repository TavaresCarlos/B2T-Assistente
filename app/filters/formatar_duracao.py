def formatar_duracao(segundos):

    segundos = int(round(segundos))

    horas = segundos // 3600

    minutos = (
        segundos % 3600
    ) // 60

    segundos_restantes = (
        segundos % 60
    )

    if horas > 0:

        if minutos > 0:
            return f"{horas} h {minutos} min"

        return f"{horas} h"

    if minutos > 0:

        if segundos_restantes > 0:
            return (
                f"{minutos} min "
                f"{segundos_restantes} s"
            )

        return f"{minutos} min"

    return f"{segundos_restantes} s"
