def say_hello_service(name: str):
    return repository.save(name.upper())