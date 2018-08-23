defmodule RelayTest do
  use ExUnit.Case, async: true, timeout: 5000

  setup_all do
    {:ok, rhost: '10.140.125.79', 
          load1: 100,
          load_max: 1000
    }
  end

  test "smoke (sanity) check" do
    Relay.start(8889)
    publish(8889,1)
    assert true == true
  end

  test "load test", context do
    assert context[:load1] !=nil
    Relay.start(7779)
    publish('localhost',7779,context[:load1])
    assert true == true
  end

  @tag external: true
  test "external load test", context do
    assert nil != context[:rhost] 
    assert nil != context[:load_max] 
    publish(context[:rhost],9999,context[:load_max])
  end

  def publish(port,n) do
    publish('localhost',port,n)
  end

  def publish(host,port,n) do
    case n>0 do
      :true -> {:ok, socket} = :gen_tcp.connect(host,port,[:binary, active: false])
        :gen_tcp.send(socket,"client socket " <> to_string n)
        :gen_tcp.close(socket)
        publish(host,port,n-1)

      :false -> IO.puts "finished port:" <> to_string port
    end
  end

end
