
ESTATUS = {1: 'Validando', 
            2: 'Validado', 
            3: 'Solicitud de Apoyo', 
            4: 'Beneficiado(a)',
            5: 'Cancelada', 
            6: 'Duplicado', 
            7: 'Rechazado', 
            8: 'Por solicitar',
            9: 'Fallecido (lista espera)', 
            10: 'Por beneficiar'}

def change_user_dict(user_dict):
    """Change the user dictionary to a better use format

        Params
        ------
        user_dict : dict
            Dictionary containing the users of the system.

        Returns
        -------
        new_user_dict
            The new user dictionary with a better use format.
        """
    new_user_dict = {}
    for index in user_dict["user"]:
        new_user_dict[user_dict["user"][index]] = {
            "password" : user_dict["pass"][index],
            "role" : user_dict["role"][index]
        }
    return new_user_dict