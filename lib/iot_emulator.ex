defmodule IotEmulator do
  require Logger
  #require Buffer

  @moduledoc """
  An IoT Receiver (server).
  Acknowledgement - Jon Yurek, 2017.
  """

  @doc """
  Spawn a TCP listener, as not to block.  Note: active=false for simplification (i.e., polling).

  ## Examples

      iex> IotEmulator.start()

  """
  def start(port) do
    spawn(fn ->
      case :gen_tcp.listen(port, [:binary, active: false, reuseaddr: true]) do
        {:ok, socket} ->
          #Logger.info("Connected.")
          accept_connection(socket)

        {:error, reason} ->
          Logger.error("Could not listen: #{reason}")
      end
    end)
  end

  @doc """
  Handles multiple concurrent connections, each spawning a read & forward.
  """
  def accept_connection(socket) do
    {:ok, client} = :gen_tcp.accept(socket)
    Logger.info("Socket Connection: ")

    spawn(fn ->
      {:ok, buffer_pid} = StringIO.open("data")
      Process.flag(:trap_exit, true)
      serve(client, buffer_pid)
    end)

    accept_connection(socket)
  end

  def serve(socket, buffer_pid) do
    case :gen_tcp.recv(socket, 0) do
      {:ok, data} ->
        buffer_pid = maybe_recreate_buffer(buffer_pid)
        IO.write(buffer_pid, data)
        #Buffer.receive(buffer_pid, data)
        serve(socket, buffer_pid)

      {:error, reason} ->
        Logger.info("Socket terminating: #{inspect(reason)}")
        IO.puts(StringIO.flush(buffer_pid))
    end
  end

  defp maybe_recreate_buffer(original_pid) do
    receive do
      {:EXIT, ^original_pid, _reason} ->
        {:ok, new_buffer_pid} = StringIO.open("data")
        IO.write(new_buffer_pid, StringIO.flush(original_pid))
        new_buffer_pid
    after
      10 ->
        original_pid
    end
  end

end
