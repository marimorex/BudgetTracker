# import asyncio
# import uvicorn

# async def main():
#     config = uvicorn.Config("api.accounts:app", port=8000, log_level="info")
#     server = uvicorn.Server(config)
#     await server.serve()

# if __name__ == "__main__":
#     asyncio.run(main())

import uvicorn


def main():
    uvicorn.run(
        "api.accounts:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    print("NOTE: If you cannot connect to the default URL at 0.0.0.0")
    print("      Try connecting to http://localhost:8000")
    main()
